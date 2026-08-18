import { GoogleGenAI } from "@google/genai";
import { NextResponse } from "next/server";

const DEMO_TEXT = "Hallo, wie geht es dir?";

export async function POST() {
  const apiKey = process.env.GEMINI_API_KEY?.trim();
  if (!apiKey) {
    return NextResponse.json(
      { error: "GEMINI_API_KEY is not set. Add it to .env.local or docker-compose." },
      { status: 500 },
    );
  }

  const model = process.env.GEMINI_MODEL?.trim() || "gemini-3.6-flash";

  try {
    const ai = new GoogleGenAI({ apiKey });
    const response = await ai.models.generateContent({
      model,
      contents: `Translate the following German text to Ukrainian. Reply with only the translation.\n\n${DEMO_TEXT}`,
    });

    const translation = response.text?.trim();
    if (!translation) {
      return NextResponse.json(
        { error: "Gemini returned an empty response." },
        { status: 502 },
      );
    }

    return NextResponse.json({
      source: DEMO_TEXT,
      translation,
      model,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Gemini request failed";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
