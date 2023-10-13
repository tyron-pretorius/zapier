function setYearlyValues() {
  
  var today = new Date();
  var mm = today.getMonth() + 1 //January is 0!

  if (mm == 1)
  {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Evergreen Campaigns");
    
    var lastColumn = sheet.getLastColumn();
    data = sheet.getRange(1,1,1,lastColumn).getValues();//Get 2D array of all values in row one
    data = data[0];//Get the first and only inner array
    column = data.indexOf('Yearly') + 1;//Arrays are zero indexed- add 1
    
    var lastRow = sheet.getLastRow();
    var values = sheet.getRange(1,column, lastRow).getValues();
    length = values.filter(String).length;
    values = sheet.getRange(2,column, length-1).getValues();
    
    var string = values.join("*");
    
    var submissions = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Submissions");
    var row = submissions.getLastRow();
    
    var ts = submissions.getRange(row, 1).getValues();
    var years = submissions.getRange(row, 4);
        
    years.setValue(string);
    
    var url = "https://hooks.zapier.com/hooks/catch/###/xxx/";
    var options = {
      "method": "post",
      "headers": {},
      "payload": {
        "Index": '0',
        "Timestamp": ts.join('')
      }
    };
    
    var response = UrlFetchApp.fetch(url, options);
  }

}
