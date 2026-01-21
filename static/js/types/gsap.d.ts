export { };

declare global {
  // GSAP is loaded globally via CDN in base.html
  const gsap: {
    set(targets: any, vars: Record<string, any>): any;
    to(targets: any, vars: Record<string, any>): any;
    timeline(vars?: Record<string, any>): any;
  };
}
