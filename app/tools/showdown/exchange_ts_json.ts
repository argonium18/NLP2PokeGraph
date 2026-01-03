import fs from "fs";
import path from "path";

// ==============================
// 出力ディレクトリ
// ==============================
const OUTPUT_BASE_DIR = path.resolve(__dirname, "./data/raw/showdown");

fs.mkdirSync(OUTPUT_BASE_DIR, { recursive: true });

// ==============================
// データ定義（ここが拡張ポイント）
// ==============================
const EXPORT_TARGETS = [
  {
    name: "typechart",
    data: () =>
      import("../../external/pokemon-showdown/data/typechart").then(
        (m) => m.TypeChart
      ),
  },
  {
    name: "abilities",
    data: () =>
      import("../../external/pokemon-showdown/data/abilities").then(
        (m) => m.Abilities
      ),
  },
  {
    name: "pokedex",
    data: () =>
      import("../../external/pokemon-showdown//data/pokedex").then(
        (m) => m.Pokedex
      ),
  },
  {
    name: "moves",
    data: () =>
      import("../../external/pokemon-showdown/data/moves").then((m) => m.Moves),
  },
  {
    name: "items",
    data: () =>
      import("../../external/pokemon-showdown/data/items").then((m) => m.Items),
  },
];

// ==============================
// 実行
// ==============================
async function exportAll() {
  for (const target of EXPORT_TARGETS) {
    const data = await target.data();

    const outputPath = path.join(OUTPUT_BASE_DIR, `${target.name}.json`);

    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), "utf-8");

    console.log(`✔ exported: ${target.name}.json`);
  }
}

exportAll().catch((err) => {
  console.error("Export failed:", err);
  process.exit(1);
});
