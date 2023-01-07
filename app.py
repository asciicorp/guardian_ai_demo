# create a streamlit app where there is a sidebar where we can select the tranformer detr model and select a video to run the model on
# the video will be displayed on the main page and the output will be displayed on the main page
import streamlit as st
from PIL import Image
import time

from utils.app import get_model, get_controls, get_image_inputs, get_video_inputs
from utils.constants import MODEL_TYPES, DEVICE_TYPES, get_model_name, APP_STYLES
from utils.video import get_output_video
from utils.image import get_output_image

st.set_page_config(page_title="GuardianAI DEMO", page_icon="public/icon.png")
st.markdown(APP_STYLES, unsafe_allow_html=True)
st.sidebar.info(
    "Purpose of this Application is to demonstrate the AI Capabilities of the [GuardianAI]() project."
)
st.sidebar.image("public/logo.png", use_column_width=True)


model_type = st.sidebar.selectbox("Select an AI Service", MODEL_TYPES)
if model_type is not None:
    device_type = st.sidebar.selectbox("Select the device", DEVICE_TYPES)
    if device_type is None:
        st.sidebar.error("Select a device")

    model_name = st.sidebar.selectbox(f"Select a {model_type} model", get_model_name(model_type))
    if model_name is not None and device_type is not None:
        model, model_info = get_model(model_type, model_name, device_type)
    else:
        st.sidebar.error("Select a model")
        model, model_info = None, None

    input_type = st.sidebar.radio("Select the Input Type", ["Image", "Video", "Stream"], horizontal=True)
    uploaded_video, video, uploaded_image, image = None, None, None, None
    if input_type == "Video":
        uploaded_video, video = get_video_inputs()
    elif input_type == "Stream":
        st.sidebar.error("Stream not supported yet")
    elif input_type == "Image":
        uploaded_image, image = get_image_inputs()

    with st.sidebar.expander("Model Parameters"):
        if model is not None: params = get_controls(model, input_type)
        else: params = None

    if params is not None:
        if input_type == "Video":
            current_video = "uploaded_video.mp4" if uploaded_video else video if video else None
            if current_video is not None:
                st.subheader("Object Detection Output Video")
                with st.spinner("Detecting objects..."):
                   time_elapsed =  get_output_video(current_video, model_type, model, params)
                st.video("output.mp4")
                st.write(f"**Inference time:** {time_elapsed:.3f} seconds")
            else:
                st.error("Upload or Select one of the sample videos")
        elif input_type == "Image":
            current_image = Image.open(uploaded_image) if uploaded_image else Image.open(image) if image else None
            if current_image is not None:
                st.subheader("Object Detection Output Image")
                with st.spinner("Detecting objects..."):
                    output_image, time_elapsed = get_output_image(current_image, model_type, model, params)
                st.image(output_image)
                st.write(f"**Inference time:** {time_elapsed:.3f} seconds")
        elif input_type == "Stream":
            st.error("Stream not supported yet")
else:
    st.sidebar.info("Please select an AI Service")
    