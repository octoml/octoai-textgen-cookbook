import React, { useState } from "react";

const SUMARIZE_URL = "http://localhost:3000/api/summarize";

export default function Home() {
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const summarizeText = (text) => {
    fetch(SUMARIZE_URL, {
      method: "POST",
      body: JSON.stringify({
        text,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setIsLoading(false);
        setSummary(data.message.content);
      });
  };

  const onLoadFile = function () {
    const typedarray = new Uint8Array(this.result);

    // Load the PDF file.
    pdfjsLib.getDocument({ data: typedarray }).promise.then((pdf) => {
      console.log("PDF loaded");

      // Fetch the first page
      pdf.getPage(1).then((page) => {
        console.log("Page loaded");

        // Get text from the page
        page.getTextContent().then((textContent) => {
          let text = "";
          textContent.items.forEach((item) => {
            text += item.str + " ";
          });

          // Display text content
          document.getElementById("pdfContent").innerText = text;
          setIsLoading(true);
          summarizeText(text);
        });
      });
    });
  };

  const onChangeFileInput = (event) => {
    const file = event.target.files[0];
    if (file.type !== "application/pdf") {
      console.error(file.name, "is not a PDF file.");
      return;
    }

    const fileReader = new FileReader();

    fileReader.onload = onLoadFile;

    fileReader.readAsArrayBuffer(file);
  };

  React.useEffect(() => {
    const fileInput = document.getElementById("file-input");
    if (fileInput) {
      fileInput.addEventListener("change", onChangeFileInput);
    }
  }, []);

  return (
    <main
      className={`flex relative min-h-screen flex-col items-center py-12 px-12`}
    >
      <div className="top-10 left-10 absolute flex items-center gap-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="27"
          height="32"
          fill="#fff"
          viewBox="0 0 27 32"
        >
          <path d="M11.489 30.134a6.703 6.703 0 0 1-2.177 1.384A6.974 6.974 0 0 1 6.744 32a6.994 6.994 0 0 1-3.745-1.08 6.493 6.493 0 0 1-2.483-2.874 6.117 6.117 0 0 1-.387-3.701 6.318 6.318 0 0 1 1.842-3.283l1.99 1.893a3.68 3.68 0 0 0-1.06 1.912 3.564 3.564 0 0 0 .23 2.15c.297.68.8 1.26 1.444 1.67a4.076 4.076 0 0 0 2.176.628 4.043 4.043 0 0 0 1.492-.28c.473-.185.902-.459 1.263-.804zM14.19.022c-1.698-.1-3.4.135-4.998.689a12.497 12.497 0 0 0-4.294 2.53 11.926 11.926 0 0 0-2.884 3.927 11.41 11.41 0 0 0-1.024 4.69c0 .239 0 .474.024.703.203 2.714 1.449 5.262 3.5 7.159l6.528 6.218 2.79 2.651 1.642 1.562a6.698 6.698 0 0 0 2.172 1.373c.811.317 1.681.48 2.56.476a6.993 6.993 0 0 0 3.746-1.078 6.49 6.49 0 0 0 2.484-2.875c.511-1.171.645-2.46.385-3.703a6.315 6.315 0 0 0-1.846-3.282l-1.98 1.903a3.68 3.68 0 0 1 1.062 1.912c.148.722.068 1.47-.23 2.15-.299.68-.802 1.26-1.446 1.67a4.075 4.075 0 0 1-2.175.628 4.034 4.034 0 0 1-1.492-.279 3.879 3.879 0 0 1-1.263-.805l-.928-.878-5.425-5.154-4.61-4.382c-1.558-1.434-2.508-3.362-2.67-5.419v-.546c.001-2.433 1.017-4.766 2.825-6.487 1.808-1.722 4.26-2.692 6.819-2.698h.568c2.446.164 4.738 1.196 6.422 2.89 1.684 1.694 2.638 3.927 2.672 6.258v.487c-.139 2.092-1.092 4.06-2.674 5.519l-4.997 4.736 1.99 1.893 4.984-4.737c2.077-1.932 3.32-4.533 3.486-7.291v-.627C25.9 8.793 24.68 5.9 22.503 3.711 20.324 1.523 17.352.204 14.19.022"></path>
        </svg>
        <span className="text-2xl">OctoAI</span>
      </div>

      <input className="hidden" id="file-input" type="file" />

      <button
        onClick={() => {
          document.getElementById("file-input").click();
        }}
        className="rounded gap-4 mt-10 text-white bg-gradient-to-tr from-orange-400 to-orange-500 px-6 py-2 pointer-events-auto z-30 flex items-center"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-10"
        >
          <path
            fillRule="evenodd"
            d="M10.5 3.75a6 6 0 0 0-5.98 6.496A5.25 5.25 0 0 0 6.75 20.25H18a4.5 4.5 0 0 0 2.206-8.423 3.75 3.75 0 0 0-4.133-4.303A6.001 6.001 0 0 0 10.5 3.75Zm2.03 5.47a.75.75 0 0 0-1.06 0l-3 3a.75.75 0 1 0 1.06 1.06l1.72-1.72v4.94a.75.75 0 0 0 1.5 0v-4.94l1.72 1.72a.75.75 0 1 0 1.06-1.06l-3-3Z"
            clipRule="evenodd"
          />
        </svg>
        <span>Upload PDF</span>
      </button>

      <div className="flex gap-5 mt-20 w-full">
        <div className="w-1/2">
          <h2 className="text-center mb-4 text-3xl text-white">Raw text</h2>
          <div className="text-white" id="pdfContent"></div>
        </div>

        <div className="w-1/2">
          <h2 className="text-center mb-4 text-3xl text-white">
            Summarized text
          </h2>
          {isLoading && (
            <p className="text-white text-center">Connecting to Octo AI...</p>
          )}
          {!isLoading && (
            <>
              <div className="text-white">{summary}</div>
            </>
          )}
        </div>
      </div>
      <div className="absolute left-0 right-0 top-0 -z-50">
        <img
          className="object-fit h-[100vh] w-full opacity-50"
          src="./background.webp"
          alt="background"
        />
      </div>
    </main>
  );
}
