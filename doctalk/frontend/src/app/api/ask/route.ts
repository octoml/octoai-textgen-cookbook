import { NextRequest } from "next/server";

export const maxDuration = 60;

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    const response = await fetch(`${process.env.API_ENDPOINT}`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        "x-api-key": `${process.env.API_KEY}`,
      },
      body: JSON.stringify({
        prompt: data.prompt,
        data_source: "pinecone_and_octoai",
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();

    return new Response(JSON.stringify(responseData));
  } catch (error) {
    console.error(error);

    return new Response(null, { status: 500 });
  }
}
