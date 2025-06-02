export const runAsyncWrapper = (callback: any) => {
  return (req: Request, res: any, next: any) => {
    callback(req, res, next).catch(next);
  };
};
