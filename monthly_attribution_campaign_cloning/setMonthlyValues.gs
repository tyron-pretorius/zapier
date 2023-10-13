function setMonthlyValues() {
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Evergreen Campaigns");
  
  var lastColumn = sheet.getLastColumn();
  data = sheet.getRange(1,1,1,lastColumn).getValues();//Get 2D array of all values in row one
  data = data[0];//Get the first and only inner array
  column = data.indexOf('Monthly') + 1;//Arrays are zero indexed- add 1
  
  var lastRow = sheet.getLastRow();
  var values = sheet.getRange(1,column, lastRow).getValues();
  length = values.filter(String).length;
  values = sheet.getRange(2,column, length-1).getValues();
  
  var months_string = values.join("*");
  
  var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Submissions");
  var row = submissions.getLastRow() + 1;

  var timestamp = submissions.getRange(row, 1);
  var months = submissions.getRange(row, 2);
  
  var ts = new Date().toLocaleString()
      
  timestamp.setValue(ts);
  months.setValue(months_string);
  
  var url = "https://hooks.zapier.com/hooks/catch/###/xxx/";
  var options = {
    "method": "post",
    "headers": {},
    "payload": {
      "Timestamp": ts,
      "Index":'0'
    }
  };
  
  var response = UrlFetchApp.fetch(url, options);
  
}
