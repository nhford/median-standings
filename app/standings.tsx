"use client";

import standings from "./standings.json";
import React, { useState } from "react";
import { handleSort, teamRow, sortkey, PAYOUT, sortIcon } from "./util";

const team_entries: teamRow[] = Object.values(standings);

export default function Standings() {
  //   return team_entries.map((team, i) => <div key={team.Team}>{team.Team}</div>);
  const [data, setData] = useState<teamRow[]>(team_entries);
  const [sorted, setSorted] = useState<{ key: sortkey; dir: "asc" | "desc" }>({
    key: "current",
    dir: "desc",
  });

  return (
    <table className="text-black w-full text-left border border-black">
      <thead className="text-wrap max-w-md">
        <tr className="text-xs sm:text-sm max-w-md text-wrap">
          {[
            { key: "team", label: "Team" },
            { key: "current", label: "Current Score" },
            { key: "projection", label: "Projected Score" },
            { key: "median", label: "Median %" },
            { key: "payout", label: "Expected Payout" },
          ].map((col) => (
            <th
              key={`label_${col.key}`}
              className="px-1 whitespace text-left"
              style={{ cursor: "pointer" }}
              onClick={() =>
                handleSort({
                  data: data,
                  setData: setData,
                  sorted: sorted,
                  setSorted: setSorted,
                  key: col.key as sortkey,
                  natural: col.key == "team" ? "desc" : "asc",
                })
              }
            >
              {col.label} {sortIcon(sorted, col.key as sortkey)}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((team) => (
          <React.Fragment key={team.team}>
            <tr className={`${team.rank <= 6 ? "bg-zinc-300" : ""} text-sm`}>
              {/* <td>
                  <img
                    className="standingsLogo"
                    src={imgPath(sport, row.abbrev)}
                    alt={row.abbrev + " Logo"}
                  ></img>
                </td> */}
              <td className="px-1 text-xs">{team.team}</td>
              <td>{team.current}</td>
              <td>{team.projection}</td>
              <td>{`${Math.round(team.median * 1000) / 10}%`}</td>
              <td>{`$${(Math.round(team.payout * PAYOUT * 100) / 100).toFixed(
                2
              )}`}</td>
            </tr>
          </React.Fragment>
        ))}
      </tbody>
    </table>
  );
}
