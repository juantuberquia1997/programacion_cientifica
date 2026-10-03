
function lemonadeChange(bills: number[]): boolean {

  let billFive = 0;
  let billTen = 0;

  for (const item of bills) {
    if (item === 5) {
      billFive++;
    } else if (item === 10) {
      if (billFive === 0) return false;
      billFive--;
      billTen++;
    } else {
      if (billFive > 0 && billTen > 0) {
        billFive--;
        billTen--;
      } else if (billFive >= 3) {
        billFive -= 3;
      } else {
        return false;
      }
    }
  }

  return true;
};
