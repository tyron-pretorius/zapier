function setMonthlyValuesPaid() {
  
 

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Paid Programs");
  
  var column = sheet.getRange('C:C');
  var values = column.getValues(); // get all data in one call
  var ct = 0;
  while ( values[ct][0] != "" ) {
    ct++;
  }
  
  var programs = sheet.getRange(2,4, ct-1).getValues();
  var programs_string = programs.join("*");
  
  
  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Paid Submissions");
  var row = submissions.getLastRow() + 1;
  
  var timestamp = submissions.getRange(row, 1);
  var months = submissions.getRange(row, 2);
  
  var ts = new Date().toLocaleString()
      
  timestamp.setValue(ts);
  months.setValue(programs_string);
  
  var url = "https://hooks.zapier.com/hooks/catch/###/xxx/";
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "Timestamp": ts,
      "Index": '0'
    }
  };
  
  var response = UrlFetchApp.fetch(url, options);
 
}
