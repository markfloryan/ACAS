export const nodes = [
  {id: 1, title: 'Java Data Types', grade: 100, lock:false},
  {id: 2, title: 'Arrays', grade: 100, lock:false},
  {id: 3, title: 'If Statements', grade: 100, lock:false},
  {id: 4, title: 'Objects', grade: 100, lock:false},
  {id: 5, title: 'References', grade: 100, lock:false},
  {id: 6, title: 'Interfaces', grade: 100, lock:false},
  {id: 7, title: 'Inheritance', grade: 100, lock:false},
  {id: 8, title: 'Loops', grade: 100, lock:false},
  {id: 9, title: 'Methods', grade: 100, lock:false},
  {id: 10, title: 'Big-OH, Omega,Theta', grade: 100, lock:false},
  {id: 11, title: 'Min-Heap', grade: 100, lock:false},
  {id: 12, title: 'Priority Queues', grade: 100},
  {id: 13, title: 'Queues', grade: 100, lock:false},
  {id: 14, title: 'Vectors', grade: 100, lock:false},
  {id: 15, title: 'Parameter Passing', grade: 100, lock:false},
  {id: 16, title: 'Recursion', grade: 100, lock:false},
  {id: 17, title: 'Exceptions', grade: 100, lock:false},
  {id: 18, title: 'Heap Sort', grade: 100, lock:false},
  {id: 19, title: 'Stacks', grade: 100, lock:false},
  {id: 20, title: 'Linked Lists', grade: 100, lock:false},
  {id: 21, title: 'Concurrency', grade: 100, lock:false},
  {id: 22, title: 'Binary Trees', grade: 100, lock:false},
  {id: 23, title: 'Hash Functions', grade: 100, lock:false},
  {id: 24, title: 'Bubble Sort', grade: 60, lock:false},
  {id: 25, title: 'Merge Sort', grade: 51, lock:false},
  {id: 26, title: 'BST', grade: 74, lock:false},
  {id: 27, title: 'Hash Tables', grade: 76, lock:false},
  {id: 28, title: 'Insertion Sort', grade: 75, lock:false},
  {id: 29, title: 'Quick Sort', grade: 10, lock:false},
  {id: 30, title: 'Hybrid Sorting', grade: 20, lock:false},
  {id: 31, title: 'AVL Trees', grade: 45, lock:false},
  {id: 32, title: 'Red-Black Trees', grade: 30, lock:true},
  {id: 33, title: 'Collision Resolution', grade: 40, lock:true}
];

export const edges = [
  {from: 1, to: 2},
  {from: 1, to: 4},
  {from: 1, to: 3},
  {from: 2, to: 14},
  {from: 2, to: 25},
  {from: 3, to: 8},
  {from: 4, to: 5},
  {from: 5, to: 6},
  {from: 5, to: 9},
  {from: 6, to: 7},
  {from: 8, to: 14},
  {from: 8, to: 20},
  {from: 9, to: 15},
  {from: 9, to: 17},
  {from: 10, to: 14},
  {from: 11, to: 18},
  {from: 12, to: 11},
  {from: 13, to: 12},
  {from: 14, to: 13},
  {from: 14, to: 19},
  {from: 14, to: 23},
  {from: 14, to: 24},
  {from: 15, to: 14},
  {from: 15, to: 16},
  {from: 16, to: 25},
  {from: 16, to: 22},
  {from: 17, to: 21},
  {from: 20, to: 19},
  {from: 20, to: 22},
  {from: 20, to: 23},
  {from: 22, to: 26},
  {from: 23, to: 27},
  {from: 24, to: 28},
  {from: 25, to: 29},
  {from: 26, to: 31},
  {from: 26, to: 32},
  {from: 27, to: 33},
  {from: 28, to: 30},
  {from: 29, to: 30}
];

export const options = (layoutMethod) => {
  return {
    interaction: {
      hover: true
    },
    layout: {
      hierarchical: {
        sortMethod: layoutMethod,
        direction: 'DU', 
        nodeSpacing: 500,
        levelSeparation: 250
      }
    },
    physics: {
      enabled: true,
      hierarchicalRepulsion: {
        nodeDistance: 350,
        centralGravity: 10,
        springLength: 100,
        springConstant: 0.003,
        damping: 0.3,
      },
    },
    nodes: {
      shape: 'box',
      color: {
        background: 'white',
        border: 'black'
      },
      size: 80
    },
    edges: {
      arrows: {
        to: {
          enabled: true,
          scaleFactor: 1.5,
          type:'arrow'
        }
      },
    }
  };
};