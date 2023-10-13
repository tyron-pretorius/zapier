function sendRows() {
  

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Customer Database");

  var rows = sheet.getDataRange().getValues();

  var names_string="";
  var orders_string="";
  var emails_string="";
  var phones_string="";

  for (var i=1;i<rows.length;i++){
    
    if(rows[i][4]==true){

      if (names_string==""){
        names_string = rows[i][0];
        orders_string = rows[i][1];
        emails_string = rows[i][2];
        phones_string = rows[i][3];
      }
      else{
        names_string = names_string+"*"+rows[i][0];
        orders_string = orders_string+"*"+rows[i][1];
        emails_string = emails_string+"*"+rows[i][2];
        phones_string = phones_string+"*"+rows[i][3];
      }


    }
  }
  
  var ts = new Date().toLocaleString()
      
  var url = "https://hooks.zapier.com/hooks/catch/65051/ojrsspj/";
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
