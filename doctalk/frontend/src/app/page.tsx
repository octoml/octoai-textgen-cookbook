import GeneratedImage from "@/components/UserChat";

export default function Home() {
  return (
    <main className="container flex-height">
      <div className="hero">
        <h1>
          Create your own
          <span style={{ display: "block" }}>RAG chat application</span>
        </h1>
      </div>
      <GeneratedImage />
      <div>
        <p className="credit">
          DocTalk is a RAG chat app built using Python + NextJS that can search, summarize, and answer questions from a set of docs. This demo uses <a href="https://www.pinecone.io/" target="_blank">Pinecone&apos;s documentation.</a></p>
        <p className="disclaimer">
          Please evaluate model response quality independently before using these
          for production use cases.
        </p>
      </div>
    </main>
  );
}
