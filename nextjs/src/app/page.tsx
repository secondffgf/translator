"use client";

import { useState } from "react";

type TranslateResult = {
  source?: string;
  translation?: string;
  model?: string;
  error?: string;
};

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TranslateResult | null>(null);

  async function handleTranslate() {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("/api/translate", { method: "POST" });
      const data: TranslateResult = await response.json();

      if (!response.ok) {
        setResult({ error: data.error ?? "Translation request failed." });
        return;
      }

      setResult(data);
    } catch {
      setResult({ error: "Could not reach the server." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen bg-zinc-50 font-sans dark:bg-zinc-950">
      <aside
        className="w-1/4 shrink-0 border-r border-zinc-200 bg-zinc-100 px-4 py-6 dark:border-zinc-800 dark:bg-zinc-900"
        aria-label="Sidebar"
      >
        <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400">Sidebar</p>
      </aside>

      <main className="flex min-h-screen w-3/4 flex-col">
        <header className="border-b border-zinc-200 bg-white px-6 py-4 dark:border-zinc-800 dark:bg-zinc-950">
          <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            {"German -> Ukrainian"}
          </p>
        </header>

        <div className="flex flex-1 flex-col items-center justify-center gap-6 px-4 py-8">
          <button
            type="button"
            onClick={handleTranslate}
            disabled={loading}
            className="rounded-full bg-zinc-900 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
          >
            {loading ? "Übersetze…" : "Übersetzen"}
          </button>

          {result?.error && (
            <p className="max-w-md text-center text-sm text-red-600 dark:text-red-400">
              {result.error}
            </p>
          )}

          {result?.translation && (
            <div className="max-w-md space-y-2 rounded-xl border border-zinc-200 bg-white p-4 text-sm dark:border-zinc-800 dark:bg-zinc-900">
              <p className="text-zinc-600 dark:text-zinc-400">
                <span className="font-medium text-zinc-900 dark:text-zinc-100">Quelle:</span>{" "}
                {result.source}
              </p>
              <p className="text-zinc-600 dark:text-zinc-400">
                <span className="font-medium text-zinc-900 dark:text-zinc-100">Übersetzung:</span>{" "}
                {result.translation}
              </p>
              {result.model && (
                <p className="text-xs text-zinc-500 dark:text-zinc-500">Model: {result.model}</p>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
