import gradio as gr
from toast import toast_reject, toast_success
import os


def annotate(image, label, target, type_img, topic, action, reason):
    image_name = os.path.basename(image) if image else None
    if action == "Submit":
        result = {
            "image": image_name,
            "class": label,
            "target": target,
            "type": type_img,
            "topic": topic,
        }
    else:  # Reject
        result = {
            "image": image_name,
            "action": action,
            "reason": reason
        }
    return result


def show_reason_reject():
    return gr.update(visible=True, value=None), gr.update(visible=True)


with gr.Blocks() as demo:
    gr.Markdown("# Harmful meme classification")

    with gr.Row():
        image = gr.Image(type="filepath", label="Meme",
                         value="https://phongvu.vn/cong-nghe/wp-content/uploads/2025/05/meme-hai-2.jpg")

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
        annotate,
        inputs=[image, label, target, type_img,
                topic, gr.State("Submit"), gr.State("")],
        outputs=output
    ).then(
        toast_success,
        inputs=[image],
        outputs=toast
    )

    # Reject → show reason + confirm
    btn_reject.click(
        show_reason_reject,
        inputs=None,
        outputs=[reject_reason, btn_confirm_reject]
    )

    # Confirm Reject → JSON + toast
    btn_confirm_reject.click(
        annotate,
        inputs=[image, label, target, type_img,
                topic, gr.State("Reject"), reject_reason],
        outputs=output
    ).then(
        toast_reject,
        inputs=[image, reject_reason],
        outputs=toast
    )

demo.launch()
