const airtable = require('airtable');

exports.handler = function(context, event, callback) {
  let responseObject = {};
  
  let memory = JSON.parse(event.Memory);
  
  const base = new airtable({
  apiKey: context.AIRTABLE_API_KEY,
  }).base(context.AIRTABLE_BASE_ID);
  const twiml = new Twilio.twiml.MessagingResponse();
  
  let first_name = memory.twilio.collected_data.ask_questions.answers.first_name.answer || 'Bob';
  let last_name = memory.twilio.collected_data.ask_questions.answers.last_name.answer || 'Smith';
  let housing_type = memory.twilio.collected_data.ask_questions.answers.housing_type.answer.toLowerCase() || 'OTHER';
  let age = memory.twilio.collected_data.ask_questions.answers.age.answer || '18';
  let population = memory.twilio.collected_data.ask_questions.answers.population.answer.toLowerCase() || 'OTHER';
  let gender = memory.twilio.collected_data.ask_questions.answers.gender.answer.toLowerCase() || 'OTHER';
  
  var ret = [];
  
  age = parseInt(age, 10);
  if(age < 26) {
    age = '12-25';
  } else {
    age = 'adult';
  }
  
  return base('houses')
    .select()
    .all()
    .then((records)=> {
      records.forEach((record) => {
        if(record.get("housing_type") == housing_type && 
          Object.values(record.get("population")).indexOf(population) > -1 &&
          Object.values(record.get("age")).indexOf(age) > -1
          )
          ret.push(record.get("name"))
      });
      let str = "";
      ret.forEach(function(item, index, array) {
        str += item;
        str + ', ';
      })
      str[(str.length-1)] = '.';
      let message = `Hi ${first_name} ${last_name}. We found these houses for you: ${ret}`
      responseObject = {
        "actions" : [ {
          "say": message
        }
        ]
      };
      callback(null, responseObject);
    })
    .catch((error) => {
      callback(error);
    });
};