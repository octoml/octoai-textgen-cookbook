# PDF Summarizer - Node JS 
This is a node js application that allows users to upload pdf files and summarize the content of the pdf file. The application uses a machine learning algorithm to summarize the pdf file.

<img src="preview.jpg"  />

## Instructions
This simple script will convert PDF files into summarized TXT files using AI. This will allow you to get a summary of a variety of files from CV's, manuals, etc.

## Getting Started
1. Run `npm install` to install modules
2. Place `.pdf` files in the `files` folder
3. Rename `.env.example` to `.env`
4. Signup [OctoAI](https://octo.ai/) and generate an API key to place in `.env` file
5. Run `npm start` in the terminal

## Dependencies
- [OctoAI](https://octo.ai/) - AI Text and Image Generation
- [NodeJs](https://nodejs.org/en/) - JavaScript Runtime
- [Pdf-parse](#) - Pure javascript cross-platform module to extract texts from PDFs
