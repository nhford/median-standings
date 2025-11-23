import Image from "next/image";
import metadata from "./metadata.json";
import Standings from "./standings";
import Footer from "./Footer";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-300 font-sans">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between px-6 md:px-16 py-4 md:py-32 bg-zinc-100 sm:items-start">
        <div className="w-full">
          <h1 className="max-w-xs text-2xl py-2 font-semibold leading-10 tracking-tight text-black">
            Week {metadata.current_week} Median Standings
          </h1>
          <div>
            <p className=" text-xs italic">
              Last updated: {metadata["last_updated"]}
            </p>
          </div>
          <Standings />
          <div className="text-right">
            <p className="text-xs inline-block bg-zinc-300">
              *gray indicates currently above median
            </p>
          </div>
          <div className="text-sm">
            <p>Approximate Update Schedule:</p>
            <p>Daily 8pm, and Sunday & Thursdays 11:30pm</p>
          </div>
          <div className="py-2">
            <Footer />
          </div>
        </div>
      </main>
    </div>
  );
}
