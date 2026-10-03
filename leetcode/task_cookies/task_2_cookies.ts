
function findContentChildren(g: number[], s: number[]): number {

  g.sort((a, b) => a - b);
  s.sort((a, b) => a - b);

  let child = 0;

  for (const cookie of s) {
    if (child === g.length) break;
    if (cookie >= g[child]) child++;
  }

  return child;
};
