export const PAYOUT = 75;

export type sortkey = "team" | "current" | "projection" | "median" | "payout";

export type teamRow = {
  team: string;
  current: number;
  projection: number;
  median: number;
  payout: number;
  logo: string;
  rank: number;
};

interface sortingHelper {
  data: teamRow[];
  setData: (rows: teamRow[]) => void;
  sorted: { key: sortkey; dir: "asc" | "desc" };
  setSorted: (sorted: { key: sortkey; dir: "asc" | "desc" }) => void;
  key: sortkey;
  natural: "asc" | "desc";
}

export function handleSort(helper: sortingHelper) {
  let dir = helper.natural;
  if (helper.sorted.key == helper.key && helper.sorted.dir == helper.natural) {
    dir = helper.natural == "desc" ? "asc" : "desc";
  }
  helper.setSorted({ key: helper.key, dir: dir });
  const i = dir == "asc" ? 1 : -1;
  helper.setData(
    [...helper.data].sort((a: teamRow, b: teamRow) =>
      a[helper.key] < b[helper.key] ? i : -i
    )
  );
}

export function sortIcon(
  sorted: { key: sortkey; dir: "asc" | "desc" },
  key: sortkey
) {
  return sorted.key === key ? (sorted.dir === "desc" ? "↓" : "↑") : "";
}

export function formatMedian(value: number) {
  return `${Math.round(value * 1000) / 10}%`;
}

export function formatPayout(value: number, payout = PAYOUT) {
  return `$${(Math.round(value * payout * 100) / 100).toFixed(2)}`;
}
