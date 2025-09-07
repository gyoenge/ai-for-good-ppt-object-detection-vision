# AI4Good Hackathon Project - Vision 
## PPT Object Detection Vision Code 

- Event: AI4Good Hackathon (March 2023)
- Theme: An AWS AI service development hackathon aligned with the UN Sustainable Development Goals (SDGs). 
- Team Idea: An assistive learning tool that **improves graphic accessibility for the visually impaired by converting elements (text, figures) from PowerPoint slides into a Braille pad-compatible format**. 
- Team Size: 5 members (1 Project Manager, 1 Frontend, 1 Backend, 2 AI)
- My Role: Implemented the **PPT Objetect detection features, utilizing AWS Custom Labels & Rekognition Service**.

### Description

This repository is dedicated to **process PPT image**, including **PPT object detection, text extraction, and diagram interpretion**. 

- `rekognition/`: code for detecting elements in PPT images using AWS Rekognition and AWS Custom Labels.
- `text_extract/`: code for extracting text information from text images using AWS Textract.
- `image_detail_compression/`: experimental code for interpreting diagrams.

### Preview

- PPT Object detection and braille pad mockup result:

<p align="center">
<img width="70%" alt="preview" src="https://github.com/user-attachments/assets/e460051f-d25f-4fea-b53e-91671c43d052" />
</p> 

- Our approach is limited to basic combinations of PowerPoint elements and does not support any overlap between them within our grid system. 
