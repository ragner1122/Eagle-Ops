import "./globals.css";

export const metadata = {
  title: "EAGLE SupportOps",
  description: "Tier-1 support operations demo"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
