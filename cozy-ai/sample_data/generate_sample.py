import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SAMPLE_TEXT = """DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING
SEMESTER VII — UNIVERSITY QUESTION BANK (2024-2025)
SUBJECT: DEEP LEARNING (CS8083)

UNIT I: FUNDAMENTALS OF DEEP NETWORKS & OPTIMIZATION

1. Define activation function. Explain why non-linear activation functions are essential in deep neural networks. [5 Marks] (2024)

2. Explain the architecture and detailed working of the Backpropagation algorithm with mathematical formulation and weight update rule. [13 Marks] (2025)

3. Compare Stochastic Gradient Descent (SGD), Batch Gradient Descent, and Adam optimizer with equations and convergence graphs. [10 Marks] (2023)

4. What is the vanishing gradient problem? How do ReLU activation and Residual connections mitigate it? [5 Marks] (2024)

5. What is overfitting? Describe three regularization techniques used to prevent overfitting in deep models. [5 Marks] (2025)

UNIT II: CONVOLUTIONAL NEURAL NETWORKS (CNN)

6. Explain the complete architecture of Convolutional Neural Networks (CNN) with neat diagram, working of convolution layer, stride, padding, pooling layer, and classification layer. [13 Marks] (2025)

7. Differentiate between Max Pooling and Average Pooling with a numerical 4x4 matrix example. [5 Marks] (2023)

8. What are the advantages of parameter sharing and translation invariance in CNNs compared to dense feed-forward networks? [5 Marks] (2024)

9. Describe the LeNet-5 architecture and explain the purpose of each layer in digit recognition. [8 Marks] (2022)

UNIT III: RECURRENT ARCHITECTURES & ATTENTION

10. Explain the architecture of Long Short-Term Memory (LSTM) networks and describe the role of Forget, Input, and Output gates. [13 Marks] (2025)

11. What is an Autoencoder? Explain the difference between standard autoencoders and Variational Autoencoders (VAEs). [8 Marks] (2024)

12. Explain the Self-Attention mechanism in Transformer architectures with Query, Key, and Value vectors and the scaled dot-product formula. [13 Marks] (2025)
"""

def generate_sample_files():
    sample_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(sample_dir, exist_ok=True)
    
    # 1. Write plain text version
    txt_path = os.path.join(sample_dir, "sample_deep_learning_qb.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_TEXT)
    print(f"Generated text question bank: {txt_path}")

    # 2. Write PDF version using reportlab
    pdf_path = os.path.join(sample_dir, "sample_question_bank.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#2C3A47')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#4B6584')
    )
    unit_style = ParagraphStyle(
        'UnitHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#205493'),
        spaceBefore=10,
        spaceAfter=6
    )
    q_style = ParagraphStyle(
        'QuestionText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E272C'),
        spaceAfter=8
    )

    story = []
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", subtitle_style))
    story.append(Paragraph("UNIVERSITY QUESTION BANK (2024-2025)", title_style))
    story.append(Paragraph("<b>SUBJECT:</b> DEEP LEARNING (CS8083)", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D1D8E0'), spaceBefore=5, spaceAfter=15))

    for line in SAMPLE_TEXT.splitlines():
        line = line.strip()
        if not line:
            continue
        if "DEPARTMENT OF" in line or "SEMESTER VII" in line or "SUBJECT:" in line:
            continue
        if line.startswith("UNIT"):
            story.append(Spacer(1, 8))
            story.append(Paragraph(f"<b>{line}</b>", unit_style))
        elif any(line.startswith(f"{i}.") for i in range(1, 20)):
            story.append(Paragraph(line, q_style))
        else:
            story.append(Paragraph(line, q_style))

    doc.build(story)
    print(f"Generated PDF question bank: {pdf_path}")

if __name__ == "__main__":
    generate_sample_files()
