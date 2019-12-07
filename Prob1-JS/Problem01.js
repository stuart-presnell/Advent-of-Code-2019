// MOVING OUT THE createProb FUNCTION FROM index.html TO SEE HOW IT WORKS
// index.html now calls this file rather than embedding this javascript directly


function addNums(a,b) {
    c = a + b;
    return c;
}


function fuel(mass) {
    // var x = mass / 3;
    return Math.floor(mass / 3) - 2;
}

function getMasses () {
    
}


// function createProb() {
//       // predicateSettings = (document.getElementById("folradio").checked);
//       predicateSettings = false;  // NOTE: Changed to remove dependence on removed radio button
//       // constructiveSettings = (document.getElementById("conradio").checked); // HAVEN'T WORKED OUT HOW TO USE THIS YET
//       var pstr = document.getElementById("probpremises").value;  // PREMISES STRING
//       pstr = pstr.replace(/^[,;\s]*/,'');
//       pstr = pstr.replace(/[,;\s]*$/,'');
//       var prems = pstr.split(/[,;\s]*[,;][,;\s]*/);  // TIDY UP THEN SPLIT BY SEPARATORS
      
//       var sofar = [];
//       // Parse each input premise, fail out if problematic, else push an element to 'sofar' array
//       for (var a=0; a<prems.length; a++) {  
//         if (prems[a] != '') {
//           var w = parseIt(fixWffInputStr(prems[a]));
//           if (!(w.isWellFormed)) {
//             alert('Premise ' + (a+1) + ', ' + fixWffInputStr(prems[a]) + ', is not well formed.');
//             return;
//             }
//           if ((predicateSettings) && (!(w.allFreeVars.length == 0))) {
//             alert('Premise ' + (a+1) + ' is not closed.');
//             return;
//           }
//           sofar.push({
//             "wffstr": wffToString(w, false),
//             "jstr": "Pr"
//           });
//         }
//       } 
//       // sofar is now an array of premises
//       // Each premise consists of 
//             // a 'wffstr' part (the proposition) and 
//             // a 'jstr' part (the justification, which is just "Pr")

//       // Check that the conclusion input string is well formed, fail out if not
//       var conc = fixWffInputStr(document.getElementById("probconc").value);
//       var cw = parseIt(conc);
//       if (!(cw.isWellFormed)) {
//         alert('The conclusion ' + fixWffInputStr(conc) + ', is not well formed.');
//         return;
//       }
//       if ((predicateSettings) && (!(cw.allFreeVars.length == 0))) {
//         alert('The conclusion is not closed.');
//         return;
//       }

//       // Make the "problabel" and "proofdetails" elements of the page visible
//       document.getElementById("problabel").style.display = "block";
//       document.getElementById("proofdetails").style.display = "block";
      
//       // Assemble the premises, separated by commas
//       var probstr = '';
//       for (var k=0; k<sofar.length; k++) {
//         probstr += prettyStr(sofar[k].wffstr);
//           if ((k+1) != sofar.length) {
//           probstr += ', ';
//         }
//       }

//       // Assemble the statement of the problem
//       document.getElementById("proofdetails").innerHTML = "Construct a proof for the argument: " + probstr + " ∴ " +  wffToString(cw, true);
      
//       // Finally, hand over the premises and conclusion to makeProof() [in proofs.js]
//       var tp = document.getElementById("theproof");
//       tp.innerHTML = '';
//       makeProof(tp, sofar, wffToString(cw, false));
//       }
