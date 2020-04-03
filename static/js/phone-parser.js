function prefixParsePhone(phone){
    if (phone.length == 10){
      if (phone.substring(0,2) == '05')
        return [true, "+972"+phone.substring(1,phone.length)]
      else
        return [false,"הקידומת של מספר הטלפון לא חוקית"]
    }
    if (phone.length == 12 && phone.substring(0,3) == '972'){
      return [true, "+"+phone]
    }
    if (phone.length == 13 && phone.substring(0,4) == '+972'){
      return [true, phone]
    }
    if (phone.length < 10){
      return [false, "המספר טלפון שהכנסת קצר מדי"]
    } 
    else if (phone.length > 10){
      return [false, "בטוח שהכנסת נכון את מספר הטלפון?"]
    } 
}

function parsePhone(phone){
  phone = phone.replace(/-/g,'');
  if (phone.length == 10){
    if (phone.substring(0,2) == '05')
      return [true, phone]
    else
      return [false,"הקידומת של מספר הטלפון לא חוקית",phone]
  } else if (phone.length > 10){
    if (phone[0] === '+'){
      return [true, '0'+phone.substring(phone.length-9,phone.length),phone]
    } else if (phone.length == 12 && phone.substring(0,3) == '972') {
      return [true, '0'+phone.substring(3,phone.length),phone]
    } else{
      return [false, "בטוח שהכנסת נכון את מספר הטלפון?",phone]
    }
  } else {
      return [false, "המספר טלפון שהכנסת קצר מדי",phone]
  }
}

function displayPhone(phone){
  return '0'+phone.slice(4,phone.length)
}