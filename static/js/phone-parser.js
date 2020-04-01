function prefixParsePhone(phone){
    if (phone.length == 10){
      if (phone.substring(0,2) == '05')
        return [true, "+972"+phone.substring(1,phone.length)]
      else
        return [false,"this is not a valid prefix for a phone number"]
    }
    if (phone.length == 12 && phone.substring(0,3) == '972'){
      return [true, "+"+phone]
    }
    if (phone.length == 13 && phone.substring(0,4) == '+972'){
      return [true, phone]
    }
    if (phone.length < 10){
      return [false, "This is too short for a mobile-phone number"]
    } 
    else if (phone.length > 10){
      return [false, "are you sure it's a valid phone number?"]
    } 
}

function parsePhone(phone){
  phone = phone.replace(/-/g,'');
  if (phone.length == 10){
    if (phone.substring(0,2) == '05')
      return [true, phone]
    else
      return [false,"this is not a valid prefix for a phone number",phone]
  } else if (phone.length > 10){
    if (phone[0] === '+'){
      return [true, '0'+phone.substring(phone.length-9,phone.length),phone]
    } else if (phone.length == 12 && phone.substring(0,3) == '972') {
      return [true, '0'+phone.substring(3,phone.length),phone]
    } else{
      return [false, "are you sure it's a valid phone number?",phone]
    }
  } else {
      return [false, "This is too short for a mobile-phone number",phone]
  }
}

function displayPhone(phone){
  return '0'+phone.slice(4,phone.length)
}