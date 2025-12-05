import jsPDF from 'jspdf';

export interface LessonPlanData {
  title: string;
  date: string;
  audience: string;
  content: string;
  scripture?: string;
}

// Simple markdown parser for PDF generation
const parseMarkdownToPDF = (pdf: jsPDF, content: string, startY: number, margin: number, maxWidth: number) => {
  const lines = content.split('\n');
  let yPosition = startY;
  const pageHeight = pdf.internal.pageSize.getHeight();
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    // Check if we need a new page
    if (yPosition > pageHeight - margin - 20) {
      pdf.addPage();
      yPosition = margin;
    }
    
    // Skip empty lines but add small spacing
    if (line === '') {
      yPosition += 3;
      continue;
    }
    
    // Handle horizontal rules (---)
    if (line.match(/^-{3,}$/)) {
      pdf.setDrawColor(156, 163, 175);
      pdf.line(margin, yPosition, margin + maxWidth, yPosition);
      yPosition += 8;
      continue;
    }
    
    // Handle headers (###, ####)
    if (line.startsWith('####')) {
      pdf.setFontSize(12);
      pdf.setTextColor(59, 130, 246); // Blue
      const headerText = line.replace(/^#+\s*/, '');
      pdf.text(headerText, margin, yPosition);
      yPosition += 8;
      continue;
    } else if (line.startsWith('###')) {
      pdf.setFontSize(14);
      pdf.setTextColor(59, 130, 246); // Blue
      const headerText = line.replace(/^#+\s*/, '');
      pdf.text(headerText, margin, yPosition);
      yPosition += 10;
      continue;
    }
    
    // Handle numbered lists
    if (line.match(/^\d+\./)) {
      pdf.setFontSize(10);
      pdf.setTextColor(0, 0, 0);
      const processedLine = processBoldText(line);
      const wrappedLines = pdf.splitTextToSize(processedLine.text, maxWidth - 10);
      
      for (let j = 0; j < wrappedLines.length; j++) {
        if (yPosition > pageHeight - margin - 20) {
          pdf.addPage();
          yPosition = margin;
        }
        pdf.text(wrappedLines[j], margin + (j === 0 ? 0 : 10), yPosition);
        yPosition += 5;
      }
      yPosition += 2;
      continue;
    }
    
    // Handle bullet points (-)
    if (line.startsWith('- ')) {
      pdf.setFontSize(10);
      pdf.setTextColor(0, 0, 0);
      const bulletText = line.replace(/^-\s*/, '• ');
      const processedLine = processBoldText(bulletText);
      const wrappedLines = pdf.splitTextToSize(processedLine.text, maxWidth - 10);
      
      for (let j = 0; j < wrappedLines.length; j++) {
        if (yPosition > pageHeight - margin - 20) {
          pdf.addPage();
          yPosition = margin;
        }
        pdf.text(wrappedLines[j], margin + (j === 0 ? 0 : 10), yPosition);
        yPosition += 5;
      }
      yPosition += 2;
      continue;
    }
    
    // Regular paragraphs
    pdf.setFontSize(10);
    pdf.setTextColor(0, 0, 0);
    const processedLine = processBoldText(line);
    const wrappedLines = pdf.splitTextToSize(processedLine.text, maxWidth);
    
    for (let j = 0; j < wrappedLines.length; j++) {
      if (yPosition > pageHeight - margin - 20) {
        pdf.addPage();
        yPosition = margin;
      }
      pdf.text(wrappedLines[j], margin, yPosition);
      yPosition += 5;
    }
    yPosition += 2;
  }
  
  return yPosition;
};

// Process bold text markers (**text**)
const processBoldText = (text: string) => {
  // For now, just remove the markdown symbols
  // jsPDF doesn't easily support mixed formatting in a single text call
  const cleanText = text
    .replace(/\*\*([^*]+)\*\*/g, '$1') // Remove bold markers
    .replace(/\*([^*]+)\*/g, '$1'); // Remove italic markers
  
  return { text: cleanText };
};

export const generateLessonPlanPDF = async (lessonData: LessonPlanData) => {
  try {
    // Create new PDF document
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 20;
    const maxWidth = pageWidth - (margin * 2);
    
    let yPosition = margin;
    
    // Add header/branding
    pdf.setFontSize(20);
    pdf.setTextColor(59, 130, 246); // Blue color
    pdf.text('Gospel Study Assistant', margin, yPosition);
    yPosition += 10;
    
    // Add horizontal line
    pdf.setDrawColor(156, 163, 175); // Gray color
    pdf.line(margin, yPosition, pageWidth - margin, yPosition);
    yPosition += 15;
    
    // Add lesson title
    pdf.setFontSize(16);
    pdf.setTextColor(0, 0, 0);
    pdf.text(lessonData.title, margin, yPosition);
    yPosition += 10;
    
    // Add lesson details
    pdf.setFontSize(12);
    pdf.setTextColor(75, 85, 99);
    pdf.text(`Date: ${lessonData.date}`, margin, yPosition);
    yPosition += 6;
    pdf.text(`Audience: ${lessonData.audience}`, margin, yPosition);
    yPosition += 6;
    
    if (lessonData.scripture) {
      pdf.text(`Scripture: ${lessonData.scripture}`, margin, yPosition);
      yPosition += 6;
    }
    
    yPosition += 10;
    
    // Parse and add lesson content using markdown parser
    parseMarkdownToPDF(pdf, lessonData.content, yPosition, margin, maxWidth);
    
    // Add footer on last page
    const totalPages = pdf.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      const footerY = pageHeight - 15;
      pdf.setFontSize(8);
      pdf.setTextColor(156, 163, 175);
      pdf.text('Generated by Gospel Study Assistant', margin, footerY);
      pdf.text(`${new Date().toLocaleDateString()} - Page ${i} of ${totalPages}`, pageWidth - margin - 50, footerY);
    }
    
    // Generate filename
    const sanitizedTitle = lessonData.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filename = `lesson_plan_${sanitizedTitle}_${lessonData.date.replace(/\s+/g, '_')}.pdf`;
    
    // Save the PDF
    pdf.save(filename);
    
    return true;
  } catch (error) {
    console.error('Error generating PDF:', error);
    throw new Error('Failed to generate PDF');
  }
};

// Alternative function for better formatting using HTML content
export const generateLessonPlanPDFFromHTML = async (
  lessonData: LessonPlanData,
  htmlContent: string
) => {
  try {
    // Create a temporary element to render the content
    const tempDiv = document.createElement('div');
    tempDiv.style.position = 'absolute';
    tempDiv.style.left = '-9999px';
    tempDiv.style.width = '210mm'; // A4 width
    tempDiv.style.fontFamily = 'Arial, sans-serif';
    tempDiv.style.fontSize = '12px';
    tempDiv.style.lineHeight = '1.4';
    tempDiv.style.color = '#000';
    tempDiv.style.backgroundColor = '#fff';
    tempDiv.style.padding = '20px';
    
    // Add styled content
    tempDiv.innerHTML = `
      <div style="margin-bottom: 20px; border-bottom: 2px solid #e5e7eb; padding-bottom: 15px;">
        <h1 style="color: #3b82f6; font-size: 24px; margin: 0 0 10px 0;">Gospel Study Assistant</h1>
        <h2 style="color: #000; font-size: 18px; margin: 0 0 10px 0;">${lessonData.title}</h2>
        <p style="color: #4b5563; margin: 5px 0;">
          <strong>Date:</strong> ${lessonData.date}<br>
          <strong>Audience:</strong> ${lessonData.audience}
          ${lessonData.scripture ? `<br><strong>Scripture:</strong> ${lessonData.scripture}` : ''}
        </p>
      </div>
      <div style="line-height: 1.6;">
        ${htmlContent}
      </div>
      <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #e5e7eb; font-size: 10px; color: #9ca3af;">
        <p>Generated by Gospel Study Assistant on ${new Date().toLocaleDateString()}</p>
      </div>
    `;
    
    document.body.appendChild(tempDiv);
    
    // Use html2canvas to convert to image, then add to PDF
    const html2canvas = (await import('html2canvas')).default;
    const canvas = await html2canvas(tempDiv, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff'
    });
    
    // Remove temporary element
    document.body.removeChild(tempDiv);
    
    // Create PDF
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgData = canvas.toDataURL('image/png');
    
    const imgWidth = 210; // A4 width in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    // If content is longer than one page, we need to handle pagination
    const pageHeight = 297; // A4 height in mm
    let heightLeft = imgHeight;
    let position = 0;
    
    // Add first page
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;
    
    // Add additional pages if needed
    while (heightLeft >= 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }
    
    // Generate filename
    const sanitizedTitle = lessonData.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filename = `lesson_plan_${sanitizedTitle}_${lessonData.date.replace(/\s+/g, '_')}.pdf`;
    
    // Save the PDF
    pdf.save(filename);
    
    return true;
  } catch (error) {
    console.error('Error generating PDF from HTML:', error);
    throw new Error('Failed to generate PDF');
  }
};