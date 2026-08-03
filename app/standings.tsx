"use client";

import standings from "./standings.json";
import { useState } from "react";
import {
  handleSort,
  teamRow,
  sortkey,
  sortIcon,
  formatMedian,
  formatPayout,
} from "./util";

const team_entries: teamRow[] = Object.values(standings);
const MEDIAN_CUTOFF = Math.floor(team_entries.length / 2);

const COLUMNS: { key: sortkey; label: string; natural: "asc" | "desc" }[] = [
  { key: "team", label: "Team", natural: "desc" },
  { key: "current", label: "Current Score", natural: "asc" },
  { key: "projection", label: "Projected Score", natural: "asc" },
  { key: "median", label: "Median %", natural: "asc" },
  { key: "payout", label: "Expected Payout", natural: "asc" },
];

export default function Standings() {
  const [data, setData] = useState<teamRow[]>(team_entries);
  const [sorted, setSorted] = useState<{ key: sortkey; dir: "asc" | "desc" }>({
    key: "current",
    dir: "desc",
  });

  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full min-w-[32rem] border border-black text-left text-black">
        <caption className="sr-only">
          Fantasy football median standings by team score, median chance, and
          expected payout
        </caption>
        <thead>
          <tr className="text-xs sm:text-sm">
            {COLUMNS.map((col) => {
              const ariaSort =
                sorted.key === col.key
                  ? sorted.dir === "asc"
                    ? "ascending"
                    : "descending"
                  : "none";

              return (
                <th
                  key={`label_${col.key}`}
                  scope="col"
                  aria-sort={ariaSort}
                  className="px-1 text-left whitespace-nowrap"
                >
                  <button
                    type="button"
                    className="inline-flex items-center gap-1 py-1 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                    onClick={() =>
                      handleSort({
                        data,
                        setData,
                        sorted,
                        setSorted,
                        key: col.key,
                        natural: col.natural,
                      })
                    }
                  >
                    <span>{col.label}</span>
                    <span aria-hidden="true" className="min-w-[0.75rem]">
                      {sortIcon(sorted, col.key)}
                    </span>
                  </button>
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {data.map((team) => {
            const aboveMedian = team.rank <= MEDIAN_CUTOFF;
            return (
              <tr
                key={team.team}
                className={`text-sm ${aboveMedian ? "bg-zinc-300" : ""}`}
              >
                <th scope="row" className="px-1 text-left text-xs font-normal">
                  {team.team}
                  {aboveMedian && (
                    <span className="sr-only"> (currently above median)</span>
                  )}
                </th>
                <td>{team.current}</td>
                <td>{team.projection}</td>
                <td>{formatMedian(team.median)}</td>
                <td>{formatPayout(team.payout)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
