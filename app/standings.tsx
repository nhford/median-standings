import standings from "./standings.json";
// import React, { useState, useEffect } from "react";

const team_entries = Object.values(standings);

export default function Standings() {
  return team_entries.map((team, i) => <div key={team.Team}>{team.Team}</div>);
  //   const [data, setData] = useState([]);
  //   const [expandedRow, setExpandedRow] = useState(null);
  //   const [sorted, setSorted] = useState({ key: "pct", dir: "asc" });
  //   const [loading, setLoading] = useState(true);
  //   const sortingUtil = [sorted, setSorted, data, setData];

  //   const toggleExpand = (rowIndex) => {
  //     setExpandedRow(expandedRow === rowIndex ? null : rowIndex); // Toggle expanded row
  //   };

  //   return (
  //     <>
  //         <table>
  //           <thead>
  //             <tr>
  //               <th colSpan={2} onClick={() => handleSort("team", sortingUtil)}>
  //                 Team
  //               </th>
  //               <th onClick={() => handleSort("pick_int", sortingUtil)}>Pick</th>
  //               <th onClick={() => handleSort("owner", sortingUtil)}>Owner</th>
  //               <th onClick={() => handleSort("pct", sortingUtil, "asc")}>
  //                 Record
  //               </th>
  //               <th style={{ cursor: "default" }}>+/-</th>
  //             </tr>
  //           </thead>
  //           <tbody>
  //             {team_entries.map((team, index) => (
  //               <React.Fragment key={team.Team}>
  //                 <tr
  //                   style={{ cursor: "pointer" }}
  //                   onClick={() => toggleExpand(index)}
  //                 >
  //                   <td>
  //                     <img
  //                       className="standingsLogo"
  //                       src={imgPath(sport, row.abbrev)}
  //                       alt={row.abbrev + " Logo"}
  //                     ></img>
  //                   </td>
  //                   <td className="teamName">{row.team}</td>
  //                   <td>{parseInt(row.pick)}</td>
  //                   <td className="ownerName">{row.owner}</td>
  //                   <td>{row.record}</td>
  //                   <td>
  //                     <button
  //                       className="expand"
  //                       onClick={(e) => {
  //                         e.stopPropagation(); // Prevent triggering the row click
  //                         toggleExpand(index);
  //                       }}
  //                     >
  //                       {expandedRow === index ? "-" : "+"}
  //                     </button>
  //                   </td>
  //                 </tr>
  //                 {expandedRow === index && (
  //                   <tr>
  //                     <td
  //                       colSpan="6"
  //                       style={{ padding: "10px", backgroundColor: "#f9f9f9" }}
  //                     >
  //                       <div>
  //                         <strong>Details for {row.team}</strong>
  //                         <p>Current Wins Pace: {row.wins_pace}</p>
  //                         <p>Preseason Over/Under: {row.ou}</p>
  //                         <p>Expected Wins by Draft Slot: {row.wins_exp}</p>
  //                       </div>
  //                     </td>
  //                   </tr>
  //                 )}
  //               </React.Fragment>
  //             ))}
  //           </tbody>
  //         </table>
  //     </>
  //   );
}
