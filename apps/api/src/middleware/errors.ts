import type { ErrorRequestHandler, RequestHandler } from "express";

/** RFC 9457 problem details. Never leaks stack traces to clients. */
export const notFound: RequestHandler = (req, res) => {
  res.status(404).type("application/problem+json").json({
    type: "about:blank",
    title: "Not Found",
    status: 404,
    instance: req.originalUrl,
  });
};

export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  const status = typeof err?.status === "number" && err.status >= 400 && err.status < 600 ? err.status : 500;
  req.log?.error({ err }, "request failed");
  res.status(status).type("application/problem+json").json({
    type: "about:blank",
    title: status === 500 ? "Internal Server Error" : String(err?.message ?? "Error"),
    status,
    instance: req.originalUrl,
  });
};
