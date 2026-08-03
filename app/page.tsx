import metadata from "./metadata.json";
import Standings from "./standings";
import Footer from "./Footer";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-300 font-sans">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between bg-zinc-100 px-6 py-4 sm:items-start md:px-16 md:py-32">
        <div className="w-full">
          <h1 className="max-w-xs py-2 text-2xl font-semibold leading-10 tracking-tight text-black">
            Week {metadata.current_week} Median Standings
          </h1>
          <p className="text-xs italic">
            Last updated: {metadata.last_updated}
          </p>
          <Standings />
          <p className="mt-1 text-right text-xs">
            <span className="inline-block bg-zinc-300 px-1">
              Gray row = currently above median
            </span>
          </p>
          <div className="mt-3 text-sm">
            <p>Approximate update schedule</p>
            <p className="text-zinc-700">
              Daily 8pm ET, plus Sunday &amp; Thursday 11:30pm ET
            </p>
          </div>
          <div className="py-2">
            <Footer />
          </div>
        </div>
      </main>
    </div>
  );
}
