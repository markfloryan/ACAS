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
      enabled: false,
      forceAtlas2Based: {
        gravitationalConstant: 1,
        centralGravity: 0.01,
        springConstant: 0.09,
        springLength: 200,
        damping: 0.4,
        avoidOverlap: 10
      },
      repulsion: {
        centralGravity: 0.0,
        springLength: 0,
        springConstant: 0.00,
        nodeDistance: 0,
        damping: 0.00
      },
      hierarchicalRepulsion: {
        centralGravity: .9,
        springLength: 750,
        springConstant: 0.02,
        nodeDistance: 375,
        damping: 0.1
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