import { getSessionCookie } from "better-auth/cookies";
import { NextRequest, NextResponse } from "next/server";

import { BASE_URL } from "./lib/server/settings";

export async function middleware(request: NextRequest) {
  const sessionCookie = getSessionCookie(request);

  if (!sessionCookie) {
    const pathname = request.nextUrl.pathname;
    if (
      pathname !== "/sign-in" &&
      pathname !== "/sign-up" &&
      pathname !== "/reset" &&
      pathname !== "/change-password" &&
      !pathname.startsWith("/check") &&
      !pathname.startsWith("/api/auth/callback") &&
      !pathname.startsWith("/healthz") &&
      !pathname.startsWith("/images")
    ) {
      const redirectPath = getUnauthenticatedRedirectPath(pathname);
      const newUrl = new URL(redirectPath, process.env.NEXT_PUBLIC_BASE_URL || BASE_URL);
      if (pathname !== "/") {
        const redirectTo = new URL(pathname, process.env.NEXT_PUBLIC_BASE_URL || BASE_URL);
        redirectTo.search = request.nextUrl.search;
        newUrl.searchParams.set("redirectTo", redirectTo.toString());
      }
      return Response.redirect(newUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};

function getUnauthenticatedRedirectPath(pathname: string) {
  if (pathname.startsWith("/o")) {
    const slug = pathname.split("/")[2];
    return `/check/${slug}`;
  } else {
    return "/sign-in";
  }
}
