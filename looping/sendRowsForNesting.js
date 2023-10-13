function sendRowsForNesting() {
  

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Customer Database Large");

  var rows = sheet.getDataRange().getValues();

  var zapier_iteration_limit = 500;

  var names_string;
  var orders_string;
  var emails_string;
  var phones_string;

  for (var i=1; i <= rows.length; i=i+zapier_iteration_limit){

     names_string="";
     orders_string="";
     emails_string="";
     phones_string="";

    for (var j=0;(j<zapier_iteration_limit) &&( (i+j) <=rows.length);j++){
      
      if (names_string==""){
        names_string = rows[i+j][0];
        orders_string = rows[i+j][1];
        emails_string = rows[i+j][2];
        phones_string = rows[i+j][3];
      }
      else{
        names_string = names_string+"*"+rows[i+j][0];
        orders_string = orders_string+"*"+rows[i+j][1];
        emails_string = emails_string+"*"+rows[i+j][2];
        phones_string = phones_string+"*"+rows[i+j][3];
      }


    }
  
  var ts = new Date().toLocaleString()
      
  var url = "https://hooks.zapier.com/hooks/catch/65051/bykfncv/"
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "Timestamp": ts,
      "Names": names_string,
      "Orders": orders_string,
      "Emails":emails_string,
      "Phones":phones_string
    }
  };
    
    var response = UrlFetchApp.fetch(url, options);
  
  }
}
