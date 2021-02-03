<script>

export function getAncestors(tree, topic_id) {
  let ret = [];
  tree.edges.forEach((edge) => {
    if (edge.topic_node == topic_id)
      ret.push(edge.ancestor_node);
  });
  return ret;
}
export function getChildren(tree, topic_id) {
  let ret = [];
  tree.edges.forEach((edge) => {
    if (edge.ancestor_node == topic_id)
      ret.push(edge.topic_node);
  });
  return ret;
}
/*function getCompetencies(topic_ids) {
  let ret = [];
  topic_ids.forEach((id) => {
    classData.nodes.forEach((node) => {
    if (node.topic.id == id)
      ret.push(node.competency);
    });
  });
  return ret;
}*/
export function getNode(tree, topic_id) {
  let ret = null;
  tree.nodes.forEach((node) => {
    //console.log(topic_id + ' ' + node.topic.id);
    if (node.topic.id == topic_id)
      ret = node;
  });
  return ret;
}
export function resolveLock(tree, parent_id, children_ids) {
  let parent_node = getNode(tree, parent_id);
  if (parent_node == null) {
    console.log('parent_node was null: ' + parent_id);
    return;
  }
  children_ids.forEach((child_id)=> {
    let child_node = getNode(tree, child_id);
    if (child_node != null) {
      child_node.topic.locked = child_node.topic.locked || parent_node.topic.locked || (parent_node.competency == 0);
    } else {
      console.log('Childnode was null: ' + child_id);
    }
  });
}

// TODO: To handle multiple, search for nodes with children but no ancestors and trickle on each
// Find root node. Hopefully there aren't multiple roots or this will fail
export function lockTree(tree) {
  let rootNode = tree.nodes[0].topic.id;
  
  let ancestors = getAncestors(tree, rootNode);
  while (ancestors.length > 0) {
    rootNode = ancestors[0];
    ancestors = getAncestors(tree, rootNode);
  }

  // Trickle down lock the tree
  let nodes = [rootNode];
  for (let i = 0; i < nodes.length; i++) {
    let children = getChildren(tree, nodes[i]);
    resolveLock(tree, nodes[i], children);

    children.forEach((child) => { nodes.push(child); });
  }
}

export default {
  getAncestors, getChildren, getNode, resolveLock, lockTree
};
</script>
