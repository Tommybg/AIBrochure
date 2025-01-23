import "@livekit/components-styles";
import "./globals.css";
import { Public_Sans } from "next/font/google";
import Image from 'next/image';

const publicSans400 = Public_Sans({
  weight: "400",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`h-full ${publicSans400.className}`}>
      <body className="h-full bg-white relative">
        <div className="absolute top-4 right-4 z-10">
          <Image 
            src="https://pbs.twimg.com/profile_images/1849229460077215744/LVO-7LYC_400x400.jpg" 
            alt="Logo" 
            width={80} 
            height={80} 
            className="rounded-full"
            priority 
          />
        </div>
        {children}
      </body>
    </html>
  );
}
