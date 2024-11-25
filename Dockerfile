FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN git clone -b main https://github.com/Kavir-AI/resemble-custom.git /app/resemble-enhance
WORKDIR /app/resemble-enhance
RUN pip install -e .
RUN pip install triton
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python", "app.py"]