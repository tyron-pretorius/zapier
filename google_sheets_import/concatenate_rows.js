function concatenateRows() {
  

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

  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Concatenated Columns");
  var row = submissions.getLastRow() + 1;
  
  var ts = new Date().toLocaleString();
  var timestamp = submissions.getRange(row, 1);
  var names = submissions.getRange(row, 2);
  var orders = submissions.getRange(row, 3);
  var emails = submissions.getRange(row, 4);
  var phones = submissions.getRange(row, 5);
      
  timestamp.setValue(ts);
  names.setValue(names_string);
  orders.setValue(orders_string);
  emails.setValue(emails_string);
  phones.setValue(phones_string);
      
  var url = "https://hooks.zapier.com/hooks/catch/65051/ojrsspj/";
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "Timestamp": ts
    }
  };
  
  var response = UrlFetchApp.fetch(url, options);
 
}
