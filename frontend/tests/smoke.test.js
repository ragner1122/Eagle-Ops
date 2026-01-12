const fs = require("fs");
const path = require("path");

const pagePath = path.join(__dirname, "..", "app", "page.tsx");
const contents = fs.readFileSync(pagePath, "utf8");

if (!contents.includes("export default function Home")) {
  throw new Error("Home component export missing in page.tsx");
}

if (!contents.includes("EAGLE SupportOps")) {
  throw new Error("Expected EAGLE SupportOps heading missing in page.tsx");
}

console.log("Frontend smoke test passed.");
