
function lemonadeChange(bills: number[]): boolean {

  let billFive = 0;
  let billTen = 0;
  let billTwenty = 0;
  let isValid = true;

  bills.forEach((item) => {
    if (!isValid) return;

    if (item === 10) {
      if (billFive > 0) {
        billTen++;
        billFive--;
      }
      else {
        isValid = false
      }
    }

    else if (item === 20) {
      if (billFive > 0 && billTen > 0) {
        billTwenty++;
        billFive--;
        billTen--;
      }
      else if (billFive > 2) {
        billTwenty++;
        billFive = billFive - 3;
      }
      else {
        isValid = false
      }
    }
    else if (item === 5) {
      billFive++;
    }

  })

  return isValid
};