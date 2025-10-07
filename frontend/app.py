import gradio as gr
import os
import requests
from toast import toast_reject, toast_success

# backend API
API_URL = "http://127.0.0.1:8000" 


def submit_to_api(image, label, target, type_img, topic, action, reason):
    if not image:
        return {"error": "No image selected"}

    files = {"image": open(image, "rb")}
    if action == "Submit":
        data = {
            "label": label,
            "target": target,
            "type_img": type_img,
            "topic": topic
        }
        resp = requests.post(
            f"{API_URL}/annotate/submit", files=files, data=data)
    else:  # Reject
        data = {"reason": reason}
        resp = requests.post(
            f"{API_URL}/annotate/reject", files=files, data=data)

    return resp.json()

# only use for rejecting
def show_reason_reject():
    return gr.update(visible=True, value=None), gr.update(visible=True)


with gr.Blocks() as demo:
    gr.Markdown("# Harmful meme classification")

    with gr.Row():
        image = gr.Image(
            type="filepath",
            label="Meme",
            value="https://phongvu.vn/cong-nghe/wp-content/uploads/2025/05/meme-hai-2.jpg"
        )

        with gr.Column():
            label = gr.Radio(["Harmful", "Harmless"],
                             label="Label", value="Harmful")
            target = gr.Radio(["individual", "organization"],
                              label="Target", value="individual")
            type_img = gr.Radio(
                ["Hate", "Offensive", "Propaganda"], label="Type", value="Hate")
            topic = gr.Radio(["politics", "pets", "life"],
                             label="Select topic", value="politics")

            with gr.Row():
                btn_submit = gr.Button("Submit")
                btn_reject = gr.Button("Reject")

            reject_reason = gr.Radio(
                ["Blurry", "Offensive Text", "Nudity", "Off-topic"],
                label="Reason for rejection",
                visible=False
            )

            btn_confirm_reject = gr.Button("Confirm Reject", visible=False)

    output = gr.JSON(label="annotation JSON")
    toast = gr.HTML()

    # Reset UI
    image.change(
        lambda: (
            gr.update(value="Harmful"),
            gr.update(value="individual"),
            gr.update(value="Hate"),
            gr.update(value="politics"),
            gr.update(visible=False, value=None),
            gr.update(visible=False),
            None,
            ""
        ),
        inputs=None,
        outputs=[label, target, type_img, topic,
                 reject_reason, btn_confirm_reject,
                 output, toast]
    )

    # Submit flow
    btn_submit.click(
        submit_to_api,
        inputs=[image, label, target, type_img,
                topic, gr.State("Submit"), gr.State("")],
        outputs=output
    ).then(
        toast_success,
        inputs=[image],
        outputs=toast
    )

    # Reject
    btn_reject.click(
        show_reason_reject,
        inputs=None,
        outputs=[reject_reason, btn_confirm_reject]
    )

    # Confirm Reject
    btn_confirm_reject.click(
        submit_to_api,
        inputs=[image, label, target, type_img,
                topic, gr.State("Reject"), reject_reason],
        outputs=output
    ).then(
        toast_reject,
        inputs=[image, reject_reason],
        outputs=toast
    )

demo.launch()
