import os

def toast_success(image):
    image_name = os.path.basename(image) if image else "Unknown"
    toast_html = f"""
    <style>
    @keyframes fadeinout {{
        0%   {{opacity: 0;}}
        10%  {{opacity: 1;}}
        80%  {{opacity: 1;}}
        100% {{opacity: 0;}}
    }}
    </style>
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #2e7d32;
        color: #ffffff;
        padding: 16px 28px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        font-weight: 700;
        font-size: 18px;
        z-index: 2147483647;
        pointer-events: none;
        animation: fadeinout 2s forwards;
    ">
        ✅ Submit successfully: <b>{image_name}</b>
    </div>
    """
    return toast_html


def toast_reject(image, reason):
    image_name = os.path.basename(image) if image else "Unknown"
    toast_html = f"""
    <style>
    @keyframes fadeinout {{
        0%   {{opacity: 0;}}
        10%  {{opacity: 1;}}
        80%  {{opacity: 1;}}
        100% {{opacity: 0;}}
    }}
    </style>
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #800000;  /* đỏ nhạt hơn */
        color: #ffffff;
        padding: 16px 28px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        font-weight: 700;
        font-size: 18px;
        z-index: 2147483647;
        pointer-events: none;
        animation: fadeinout 2s forwards; /* tổng 4s: 0.4s fade-in, 2.8s hiện rõ, 0.8s fade-out */
    ">
        ✅ Reject successfully: <b>{image_name}</b> (Reason: {reason})
    </div>
    """
    return toast_html
