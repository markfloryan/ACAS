export const nodes = [
];

export const edges = [
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
    manipulation: {
      addNode: function (data, callback) {
        console.log(this);
        // this.$emit('onOpen');
        
      },
      editNode: function (data, callback) {
        // filling in the popup DOM elements
        
      },
      addEdge: function (data, callback) {
        if (data.from == data.to) {
          var r = confirm('Do you want to connect the node to itself?');
          if (r == true) {
            callback(data);
          }
        }
        else {
          callback(data);
        }
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