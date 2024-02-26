import GeneratedImage from "@/components/UserChat";

export default function Home() {
  return (
    <main className="container flex-height">
      <div className="hero">
        <h1>
          <span style={{ display: "block" }}>AskTechnically</span>
        </h1>
      </div>
      <GeneratedImage />
      <div>
        <p className="credit">
          AskTechnically is a RAG chat app built using Python + NextJS that can search and answer questions from a set of docs. This demo is
          utilizing articles from{" "}
          <a href="https://technically.dev/" target="_blank">
            technically.dev.
          </a>
        </p>
      </div>
    </main>
  );
}
