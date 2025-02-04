const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Directory to save the PDFs
const outputDir = './pdfs';
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

// Read URLs from urls.txt
const urls = fs.readFileSync('urls.txt', 'utf8').split('\n').filter(url => url.trim() !== '');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    for (let i = 0; i < urls.length; i++) {
        const url = urls[i].trim();
        const outputPdf = path.join(outputDir, `chapter-${String(i + 1).padStart(2, '0')}.pdf`);

        console.log(`Processing: ${url} -> ${outputPdf}`);

        await page.goto(url, { waitUntil: 'networkidle2' });

        await page.pdf({
            path: outputPdf,
            format: 'A4',
            printBackground: true,
            displayHeaderFooter: false, // Disable headers and footers
            margin: {
                top: '1cm',
                bottom: '1cm',
                left: '1cm',
                right: '1cm'
            }
        });
    }

    await browser.close();
    console.log('✅ PDF generation complete!');
})();
