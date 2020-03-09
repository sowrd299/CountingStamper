
// the different types of stamps
// "stamps" are markers put on cells of the game board

class Stamp{

    constructor(id, color){
        this.id = id;
        this.color = color;
    }

    should_stamp(cell){
        return cell.stamp == this.id;
    }

    render(canvas,x,y,x2,y2){
        var w = x2-x;
        var h = y2-y;
        var ctx = canvas.getContext("2d");
        var radius = Math.min(w,h)/2;

        // actually drawing the stamp
        ctx.beginPath();
        ctx.arc(x + (w)/2, y + (h)/2, radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

}

/**
 * A version of stamp whose condition is that
 *  a cells "value" matches the "value" of a given object
 */
class ValueStamp extends Stamp{

    /**
     * Takes the target object to compare values with
     */
    constructor(target, color){
        super(0, color);
        this.target = target;
    }

    should_stamp(cell){
        return cell.value == this.target.value;
    }

}

let STAMP_HAVE = new Stamp("HAVE", "#FF0000");
let STAMP_NONE = new Stamp("NONE", "#00000000");
let STAMP_WRONG = new Stamp("WRONG", "#00000050")
let STAMP_ANSWER = null;

/**
 * Returns the divisions of space on the grid
 * Takes the width and number of collumns in the grid
 * Give height and rows for y divisions
 */
function grid_coords(width, cols=5){
    var r = [];
    for(var i = 0; i < cols+1; i++){
        r.push((width / cols) * (i));
    }
    return r;
}


/**
 * Returns the index of the column the given pixel falls in
 * Can also be used for y coords
 * Any click not cleanly in a cell is undefined behavior
 */
function screen_to_grid(x, width, cols = 5){
    var x_cutoffs = grid_coords(width, cols);
    for(var i = 0; i < x_cutoffs.length; i++){
        if(x < x_cutoffs[i]){
            return i-1;
        }
    }
    return x_cutoffs.length;
}


/**
 * Draws a bingo board on the given canvas
 */
function render_board(canvas, input, cells, stamps){

    // setup and render the background
    var ctx = canvas.getContext("2d");
    ctx.fillStyle = "#F0F0E5";
    ctx.fillRect(0,0,canvas.width, canvas.height);

    // setup the grid
    var xs = grid_coords(canvas.width);
    var ys = grid_coords(canvas.height);

    // draw the grid
    ctx.beginPath();
    for(var i = 0; i < xs.length; i++){

        // vertical lines
        ctx.moveTo(xs[i],0);
        ctx.lineTo(xs[i],canvas.height);

        // horizontal lines
        ctx.moveTo(0,ys[i]);
        ctx.lineTo(canvas.width,ys[i]);
    }
    ctx.stroke();

    // render the cells and stamps
    var margin = 10;
    for(var i = 0; i < cells.length; i++){ // for each column
        for(var j = 0; j < cells[i].length; j++){ // for each cell in that column
            // text
            ctx.font = "24px Arial";
            ctx.fillStyle = "#000";
            ctx.fillText(cells[i][j].value, xs[i] + margin, ys[j+1] - margin);
            // stamps
            for(var k = 0; k < stamps.length; k++){
                if(stamps[k].should_stamp(cells[i][j])){
                    stamps[k].render(canvas, xs[i], ys[j], xs[i+1], ys[j+1]);
                }
            }
        }
    }

}


/**
 * To be called when the game board canvas is clicked on
 * Takes the event, the canvas, the input tag to store the clicked data to,
 *  and a list of all the cell objects
 */
function board_onclick(event, canvas, input, cells){
    // get the cell clicked on
    var rect = canvas.getBoundingClientRect();
    var x = screen_to_grid(event.clientX - rect.left, canvas.width);
    var y = screen_to_grid(event.clientY - rect.top, canvas.height);
    // update the cell data, unless there is already a stamp there
    if(cells[x][y].stamp == STAMP_NONE.id){
        input.value = cells[x][y].value;
    }
}


/**
 * sets up a canvas and input node to represent a bingo board
 */
function setup_board(canvas, input, cells){

    STAMP_ANSWER = new ValueStamp(input, "#0000FF50")

    // attack the onclick
    canvas.onclick = function(canvas, input, cells){
        return function(event){
            board_onclick(event, canvas, input, cells);
            render_board(canvas, input, cells, [STAMP_HAVE, STAMP_WRONG, STAMP_ANSWER]);
        };
    }(canvas, input, cells);

    // initial render
    render_board(canvas, input, cells, [STAMP_HAVE, STAMP_WRONG]);
}