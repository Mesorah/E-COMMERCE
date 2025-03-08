export class ValidateCPF {
    constructor(sentCpf) {
      Object.defineProperty(this, 'cleanCpf', {
        writable: false,
        enumerable: true,
        configurable: false,
        value: sentCpf.replace(/\D+/g, '')
      });
    }
  
    isSequence() {
      return this.cleanCpf.charAt(0).repeat(11) === this.cleanCpf;
    }
  
    genNewCPF() {
      const cpfWithoutDigits = this.cleanCpf.slice(0, -2);
      const digit1 = ValidateCPF.genDigit(cpfWithoutDigits);
      const digit2 = ValidateCPF.genDigit(cpfWithoutDigits + digit1);
      this.newCPF = cpfWithoutDigits + digit1 + digit2;
    }
  
    static genDigit(cpfWithoutDigits) {
      let total = 0;
      let reverse = cpfWithoutDigits.length + 1;
  
      for (let numericString of cpfWithoutDigits) {
        total += reverse * Number(numericString);
        reverse--;
      }
  
      const digit = 11 - (total % 11);
      return digit <= 9 ? String(digit) : '0';
    }
  
    validate() {
      if (!this.cleanCpf) return false;
      if (typeof this.cleanCpf !== 'string') return false;
      if (this.cleanCpf.length !== 11) return false;
      if (this.isSequence()) return false;
      this.genNewCPF();
  
      return this.newCPF === this.cleanCpf;
    }
  }
  