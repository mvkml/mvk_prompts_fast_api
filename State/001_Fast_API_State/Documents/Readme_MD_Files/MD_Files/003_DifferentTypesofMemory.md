# Different Types of Memory in AI Systems

## Developer Profile

**Name:** Vishnu Kiran M  
**Role:** End-to-End AI, Cloud & Big Data Solution Designer  
**Project:** VishAgent - MARVISH Industrial AI Assistant

---

## Overview of Memory Types in AI

Memory in AI systems comes in different types, each serving specific purposes. Understanding these types helps in building more effective AI applications that can learn, remember, and make better decisions.

---

## 1. Short-Term Memory (Working Memory)

### Definition
Temporary storage for immediate processing needs, similar to RAM in computers.

### Characteristics
- **Capacity**: Limited (typically 5-10 items)
- **Duration**: Minutes to hours
- **Speed**: Very fast access
- **Purpose**: Current task execution
- **Volatility**: Lost when session ends

### Use Cases
- Current conversation context
- Ongoing task state
- Immediate decision-making
- Real-time processing

### Implementation
```python
from collections import deque
from datetime import datetime

class ShortTermMemory:
    def __init__(self, max_size: int = 10):
        self.messages = deque(maxlen=max_size)
        self.max_size = max_size
    
    def add(self, role: str, content: str, timestamp: datetime = None):
        """Add message to short-term memory"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp or datetime.now()
        })
    
    def get_all(self):
        """Get all messages in order"""
        return list(self.messages)
    
    def get_last_n(self, n: int):
        """Get last n messages"""
        return list(self.messages)[-n:]
    
    def clear(self):
        """Clear short-term memory"""
        self.messages.clear()
    
    def context_window(self):
        """Get formatted context for LLM"""
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])
```

### Example in VishAgent
```python
# Managing current claim analysis conversation
stm = ShortTermMemory(max_size=20)
stm.add("user", "Analyze claim CLM_123")
stm.add("assistant", "I'll analyze this claim...")
stm.add("tool", "Policy status: Active, Coverage: $10,000")
stm.add("assistant", "The claim appears eligible...")

# Get context for next LLM call
context = stm.context_window()
```

---

## 2. Long-Term Memory (Episodic Memory)

### Definition
Persistent storage of past experiences, conversations, and outcomes indexed and retrievable.

### Characteristics
- **Capacity**: Large (unlimited with database)
- **Duration**: Permanent
- **Speed**: Medium (database lookups)
- **Purpose**: Learning from history
- **Persistence**: Survives across sessions

### Use Cases
- User interaction history
- Past decision outcomes
- Claim analysis history
- Customer behavior patterns
- Audit trails and compliance

### Implementation
```python
from datetime import datetime
from typing import List, Dict, Optional

class LongTermMemory:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def store_episode(self, session_id: str, episode: Dict):
        """Store complete interaction episode"""
        self.db.insert("episodes", {
            "session_id": session_id,
            "timestamp": datetime.now(),
            "messages": episode.get("messages", []),
            "outcome": episode.get("outcome"),
            "entities": episode.get("entities", []),
            "metadata": episode.get("metadata", {})
        })
    
    def retrieve_episode(self, episode_id: str) -> Optional[Dict]:
        """Retrieve specific episode"""
        return self.db.query_one(
            "SELECT * FROM episodes WHERE id = ?",
            episode_id
        )
    
    def retrieve_user_history(self, user_id: str, limit: int = 50):
        """Get all episodes for user"""
        return self.db.query(
            "SELECT * FROM episodes WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            user_id, limit
        )
    
    def retrieve_similar_episodes(self, query: str, limit: int = 5):
        """Find similar past interactions"""
        return self.db.query(
            """SELECT * FROM episodes 
               WHERE similarity(messages, ?) > 0.7 
               LIMIT ?""",
            query, limit
        )
    
    def get_statistics(self, user_id: str) -> Dict:
        """Get user statistics from history"""
        return self.db.query_one(
            """SELECT 
               COUNT(*) as total_interactions,
               AVG(outcome) as avg_success,
               MAX(timestamp) as last_interaction
               FROM episodes WHERE session_id = ?""",
            user_id
        )
```

### Example in VishAgent
```python
# Store claim analysis episode
ltm.store_episode(
    session_id="USER_123",
    episode={
        "messages": conversation_history,
        "outcome": "claim_approved",
        "entities": {
            "claim_id": "CLM_456",
            "user_id": "USER_123",
            "amount": 5000
        },
        "metadata": {
            "model_used": "gpt-4",
            "confidence": 0.95,
            "processing_time": 2.5
        }
    }
)

# Retrieve user's claim history
user_history = ltm.retrieve_user_history("USER_123", limit=20)

# Find similar past claims
similar = ltm.retrieve_similar_episodes("policy coverage review")
```

---

## 3. Semantic Memory

### Definition
General knowledge, facts, and conceptual relationships stored as embeddings and structured knowledge bases.

### Characteristics
- **Capacity**: Large (vector databases)
- **Duration**: Permanent
- **Speed**: Medium (vector search)
- **Purpose**: Knowledge retrieval
- **Structure**: Embeddings + relationships

### Use Cases
- Domain knowledge base
- Policy and procedure information
- Entity embeddings
- Conceptual relationships
- Language understanding

### Implementation
```python
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self, vector_store, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.vector_store = vector_store
        self.model = SentenceTransformer(embedding_model)
    
    def encode(self, text: str) -> np.ndarray:
        """Convert text to embeddings"""
        return self.model.encode(text)
    
    def store_knowledge(self, 
                       concept: str, 
                       definition: str,
                       category: str = None,
                       relationships: Dict = None):
        """Store semantic knowledge"""
        embedding = self.encode(definition)
        
        self.vector_store.add(
            ids=[concept],
            embeddings=[embedding.tolist()],
            documents=[definition],
            metadatas=[{
                "concept": concept,
                "category": category,
                "relationships": relationships or {}
            }]
        )
    
    def retrieve_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve related knowledge by semantic similarity"""
        query_embedding = self.encode(query)
        
        results = self.vector_store.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        return [
            {
                "concept": results["ids"][0][i],
                "definition": results["documents"][0][i],
                "similarity": results["distances"][0][i],
                "metadata": results["metadatas"][0][i]
            }
            for i in range(len(results["ids"][0]))
        ]
    
    def find_relationships(self, concept: str) -> Dict:
        """Find related concepts"""
        knowledge = self.vector_store.get(ids=[concept])
        if knowledge and knowledge["metadatas"]:
            return knowledge["metadatas"][0].get("relationships", {})
        return {}
```

### Example in VishAgent
```python
# Store insurance policy knowledge
semantic_memory.store_knowledge(
    concept="claim_eligibility",
    definition="A claim is eligible if the policy is active, within coverage period, and premium is paid",
    category="insurance_rules",
    relationships={
        "requires": ["active_policy", "coverage_period", "premium_payment"],
        "affects": ["claim_approval", "payout_amount"]
    }
)

# Retrieve related knowledge
knowledge = semantic_memory.retrieve_knowledge(
    query="when can customer claim insurance",
    top_k=5
)

# Find relationships
relationships = semantic_memory.find_relationships("claim_eligibility")
```

---

## 4. Procedural Memory

### Definition
Learned skills, procedures, and workflow patterns - "how to" knowledge.

### Characteristics
- **Capacity**: Medium
- **Duration**: Permanent
- **Speed**: Fast (execution)
- **Purpose**: Task automation
- **Execution**: Step-by-step workflows

### Use Cases
- Claim validation workflow
- Multi-step problem solving
- Business process automation
- Tool calling sequences
- Decision trees

### Implementation
```python
from typing import List, Callable, Dict, Any
from enum import Enum

class StepType(Enum):
    EXTRACT = "extract"
    VALIDATE = "validate"
    CALCULATE = "calculate"
    DECISION = "decision"
    EXECUTE = "execute"

class ProceduralMemory:
    def __init__(self):
        self.procedures: Dict[str, Dict] = {}
        self.step_handlers: Dict[StepType, Callable] = {}
    
    def register_procedure(self, 
                          name: str, 
                          steps: List[Dict],
                          description: str = None):
        """Register a new procedure"""
        self.procedures[name] = {
            "steps": steps,
            "description": description,
            "success_count": 0,
            "failure_count": 0,
            "avg_execution_time": 0
        }
    
    def register_step_handler(self, step_type: StepType, handler: Callable):
        """Register custom handler for step type"""
        self.step_handlers[step_type] = handler
    
    def execute_procedure(self, name: str, inputs: Dict) -> Dict:
        """Execute a procedure"""
        if name not in self.procedures:
            raise ValueError(f"Procedure '{name}' not found")
        
        procedure = self.procedures[name]
        results = []
        current_state = inputs.copy()
        
        try:
            for step in procedure["steps"]:
                result = self._execute_step(step, current_state)
                results.append(result)
                current_state.update(result)
            
            procedure["success_count"] += 1
            
            return {
                "status": "success",
                "procedure": name,
                "steps": results,
                "final_output": current_state
            }
        
        except Exception as e:
            procedure["failure_count"] += 1
            return {
                "status": "failed",
                "procedure": name,
                "error": str(e),
                "completed_steps": len(results)
            }
    
    def _execute_step(self, step: Dict, context: Dict) -> Dict:
        """Execute single step"""
        step_type = StepType(step.get("type"))
        
        if step_type in self.step_handlers:
            return self.step_handlers[step_type](step, context)
        
        # Default handlers
        if step_type == StepType.EXTRACT:
            return self._extract_step(step, context)
        elif step_type == StepType.VALIDATE:
            return self._validate_step(step, context)
        elif step_type == StepType.CALCULATE:
            return self._calculate_step(step, context)
        elif step_type == StepType.DECISION:
            return self._decision_step(step, context)
        
        return {}
    
    def _extract_step(self, step: Dict, context: Dict) -> Dict:
        """Extract specified fields"""
        fields = step.get("fields", [])
        return {f: context.get(f) for f in fields}
    
    def _validate_step(self, step: Dict, context: Dict) -> Dict:
        """Validate context against rules"""
        rules = step.get("rules", [])
        return {
            "validations": {rule: self._check_rule(rule, context) 
                           for rule in rules},
            "is_valid": all(self._check_rule(rule, context) 
                           for rule in rules)
        }
    
    def _calculate_step(self, step: Dict, context: Dict) -> Dict:
        """Execute calculation"""
        # Implementation depends on specific calculation
        return {}
    
    def _decision_step(self, step: Dict, context: Dict) -> Dict:
        """Make decision based on conditions"""
        return {}
    
    def _check_rule(self, rule: str, context: Dict) -> bool:
        """Check if rule is satisfied"""
        # Implementation for rule checking
        return True
    
    def get_procedure_stats(self, name: str) -> Dict:
        """Get statistics for procedure"""
        if name not in self.procedures:
            return {}
        
        proc = self.procedures[name]
        total = proc["success_count"] + proc["failure_count"]
        
        return {
            "name": name,
            "total_executions": total,
            "success_rate": proc["success_count"] / total if total > 0 else 0,
            "avg_execution_time": proc.get("avg_execution_time", 0)
        }
```

### Example in VishAgent
```python
# Define claim analysis procedure
claim_procedure = [
    {
        "type": "extract",
        "fields": ["claim_id", "policy_number", "amount", "description"]
    },
    {
        "type": "validate",
        "rules": ["policy_active", "within_coverage", "premium_paid"]
    },
    {
        "type": "calculate",
        "formula": "eligible_amount = min(amount, coverage_limit - paid)"
    },
    {
        "type": "decision",
        "conditions": [
            {"if": "eligible_amount > 0", "then": "approve"},
            {"if": "eligible_amount == 0", "then": "deny"},
            {"else": "review"}
        ]
    }
]

procedural_memory.register_procedure(
    "analyze_claim",
    claim_procedure,
    "Standard claim analysis workflow"
)

# Execute procedure
result = procedural_memory.execute_procedure(
    "analyze_claim",
    {
        "claim_id": "CLM_001",
        "policy_number": "POL_123",
        "amount": 5000,
        "description": "Car accident claim"
    }
)
```

---

## 5. Associative Memory

### Definition
Maps concepts and entities to their relationships and associated information.

### Characteristics
- **Capacity**: Medium to Large
- **Duration**: Permanent
- **Speed**: Very fast (key-value lookup)
- **Purpose**: Relationship retrieval
- **Structure**: Graph-like connections

### Use Cases
- Customer-policy relationships
- Claim-entity relationships
- Entity linking
- Knowledge graphs
- Pattern associations

### Implementation
```python
from typing import List, Dict, Set
from collections import defaultdict

class AssociativeMemory:
    def __init__(self):
        self.associations: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_associations: Dict[str, Set[str]] = defaultdict(set)
    
    def associate(self, 
                  entity1: str, 
                  entity2: str, 
                  relationship: str = "related"):
        """Create bidirectional association"""
        forward_key = f"{entity1}:{relationship}"
        reverse_key = f"{entity2}:{relationship}:reverse"
        
        self.associations[forward_key].add(entity2)
        self.associations[reverse_key].add(entity1)
    
    def retrieve_associations(self, 
                             entity: str, 
                             relationship: str = None) -> Dict[str, Set[str]]:
        """Retrieve all associations for entity"""
        if relationship:
            key = f"{entity}:{relationship}"
            return {relationship: self.associations.get(key, set())}
        else:
            result = {}
            for key in self.associations:
                if key.startswith(f"{entity}:"):
                    rel = key.split(":")[1]
                    result[rel] = self.associations[key]
            return result
    
    def find_path(self, 
                  start: str, 
                  end: str, 
                  max_depth: int = 3) -> List[List[str]]:
        """Find association paths between entities"""
        paths = []
        visited = set()
        
        def dfs(current: str, target: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            if current == target:
                paths.append(path + [current])
                return
            
            if current in visited:
                return
            
            visited.add(current)
            
            # Get all associations from current entity
            for rel_key in self.associations:
                if rel_key.startswith(f"{current}:"):
                    for next_entity in self.associations[rel_key]:
                        if next_entity not in visited:
                            dfs(next_entity, target, path + [current], depth + 1)
            
            visited.remove(current)
        
        dfs(start, end, [], 0)
        return paths
    
    def get_related_entities(self, entity: str, depth: int = 1) -> Set[str]:
        """Get all entities related at specific depth"""
        related = set()
        current_level = {entity}
        visited = {entity}
        
        for _ in range(depth):
            next_level = set()
            for ent in current_level:
                for key in self.associations:
                    if key.startswith(f"{ent}:"):
                        for related_ent in self.associations[key]:
                            if related_ent not in visited:
                                next_level.add(related_ent)
                                visited.add(related_ent)
            current_level = next_level
            related.update(next_level)
        
        return related
```

### Example in VishAgent
```python
# Create associations
assoc_mem = AssociativeMemory()

# User relationships
assoc_mem.associate("USER_123", "CLM_001", "filed")
assoc_mem.associate("USER_123", "CLM_002", "filed")
assoc_mem.associate("USER_123", "POL_456", "owns")

# Claim relationships
assoc_mem.associate("CLM_001", "POL_456", "covered_by")
assoc_mem.associate("CLM_001", "PERSON_001", "involves")
assoc_mem.associate("CLM_001", "VEHICLE_001", "damage_to")

# Retrieve relationships
user_claims = assoc_mem.retrieve_associations("USER_123", "filed")
# Returns: {"filed": {"CLM_001", "CLM_002"}}

# Find path
path = assoc_mem.find_path("USER_123", "VEHICLE_001")
# Returns: [["USER_123", "CLM_001", "VEHICLE_001"]]

# Related entities
related = assoc_mem.get_related_entities("USER_123", depth=2)
```

---

## 6. Attention-Based Memory

### Definition
Dynamically focuses on the most relevant information using attention mechanisms and scoring.

### Characteristics
- **Capacity**: Medium
- **Duration**: Session-based
- **Speed**: Medium
- **Purpose**: Relevance filtering
- **Mechanism**: Scoring and ranking

### Use Cases
- Context selection for LLM
- Relevant document retrieval
- Important information highlighting
- Multi-document summarization

### Implementation
```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class AttentionMemory:
    def __init__(self):
        self.memory_items: List[Dict] = []
    
    def store_with_importance(self, 
                             content: str,
                             importance: float = 0.5,
                             category: str = None,
                             metadata: Dict = None):
        """Store item with importance score"""
        self.memory_items.append({
            "content": content,
            "importance": importance,
            "category": category,
            "metadata": metadata or {},
            "access_count": 0,
            "last_accessed": None,
            "created_at": datetime.now()
        })
    
    def attend(self, 
              query: str, 
              top_k: int = 5,
              recency_weight: float = 0.2,
              importance_weight: float = 0.3,
              relevance_weight: float = 0.5) -> List[Dict]:
        """Retrieve most relevant items using attention"""
        
        scored_items = []
        for item in self.memory_items:
            attention_score = self._compute_attention(
                query, item,
                recency_weight, importance_weight, relevance_weight
            )
            scored_items.append({
                **item,
                "attention_score": attention_score
            })
        
        # Sort and get top k
        top_items = sorted(
            scored_items,
            key=lambda x: x["attention_score"],
            reverse=True
        )[:top_k]
        
        # Update access stats
        for item in top_items:
            item["access_count"] += 1
            item["last_accessed"] = datetime.now()
        
        return top_items
    
    def _compute_attention(self, 
                          query: str,
                          item: Dict,
                          recency_weight: float,
                          importance_weight: float,
                          relevance_weight: float) -> float:
        """Compute attention weight for item"""
        
        relevance_score = self._semantic_similarity(query, item["content"])
        importance_score = item["importance"]
        recency_score = self._recency_score(item["last_accessed"])
        
        return (
            relevance_weight * relevance_score +
            importance_weight * importance_score +
            recency_weight * recency_score
        )
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between texts"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])
        return cosine_similarity(vectors[0], vectors[1])[0][0]
    
    def _recency_score(self, last_accessed: Optional[datetime]) -> float:
        """Compute recency score (0-1, higher is more recent)"""
        if last_accessed is None:
            return 0.1
        
        age = datetime.now() - last_accessed
        max_age = timedelta(days=30)
        
        if age > max_age:
            return 0.0
        
        return 1.0 - (age.total_seconds() / max_age.total_seconds())
    
    def update_importance(self, content: str, new_importance: float):
        """Update importance of stored item"""
        for item in self.memory_items:
            if item["content"] == content:
                item["importance"] = new_importance
                break
```

### Example in VishAgent
```python
# Store documents with importance
attention_mem = AttentionMemory()

attention_mem.store_with_importance(
    content="Policy CLM_001 covers accident damages up to $10,000",
    importance=0.9,
    category="policy",
    metadata={"policy_id": "POL_123"}
)

attention_mem.store_with_importance(
    content="Customer has 5 previous claims in last 2 years",
    importance=0.7,
    category="history"
)

# Retrieve relevant information for current query
relevant = attention_mem.attend(
    query="what is coverage limit for accident",
    top_k=3,
    relevance_weight=0.6,
    importance_weight=0.3,
    recency_weight=0.1
)
```

---

## 7. Hierarchical Memory

### Definition
Organizes information in nested levels of abstraction for efficient search and retrieval.

### Characteristics
- **Capacity**: Large
- **Duration**: Permanent
- **Speed**: Medium
- **Purpose**: Organized storage
- **Structure**: Tree/hierarchical

### Use Cases
- Organizational structures
- Category hierarchies
- Timeline organization
- Decision trees
- Taxonomy-based storage

### Implementation
```python
from typing import Any, List, Dict

class HierarchicalMemory:
    def __init__(self):
        self.hierarchy: Dict[str, Any] = {}
    
    def store_hierarchical(self, 
                          path: List[str], 
                          data: Any,
                          metadata: Dict = None):
        """Store data at hierarchical path"""
        current = self.hierarchy
        
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[path[-1]] = {
            "data": data,
            "metadata": metadata or {},
            "created_at": datetime.now()
        }
    
    def retrieve_level(self, path: List[str]) -> Dict:
        """Retrieve all data at specific level"""
        current = self.hierarchy
        
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return {}
        
        return current if isinstance(current, dict) else {}
    
    def retrieve_branch(self, path: List[str]) -> Dict:
        """Retrieve entire branch from level"""
        return self.retrieve_level(path)
    
    def list_at_level(self, path: List[str]) -> List[str]:
        """List keys at specific level"""
        level = self.retrieve_level(path)
        return list(level.keys())
    
    def search_path(self, search_term: str, max_depth: int = 10) -> List[List[str]]:
        """Search for items by key"""
        results = []
        
        def dfs(current: Dict, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            for key, value in current.items():
                new_path = path + [key]
                
                if search_term.lower() in key.lower():
                    results.append(new_path)
                
                if isinstance(value, dict) and "data" not in value:
                    dfs(value, new_path, depth + 1)
        
        dfs(self.hierarchy, [], 0)
        return results
```

### Example in VishAgent
```python
# Hierarchical storage
hier_mem = HierarchicalMemory()

# Store claims hierarchically
hier_mem.store_hierarchical(
    ["claims", "2024", "january", "CLM_001"],
    {
        "amount": 5000,
        "status": "approved",
        "claimant": "John Doe"
    }
)

hier_mem.store_hierarchical(
    ["claims", "2024", "january", "CLM_002"],
    {
        "amount": 7500,
        "status": "pending",
        "claimant": "Jane Smith"
    }
)

hier_mem.store_hierarchical(
    ["users", "USER_123"],
    {
        "name": "John Doe",
        "email": "john@example.com",
        "policies": ["POL_456", "POL_789"]
    }
)

# Retrieve all January 2024 claims
jan_claims = hier_mem.retrieve_level(["claims", "2024", "january"])

# List all users
users = hier_mem.list_at_level(["users"])

# Search for claims
results = hier_mem.search_path("CLM_", max_depth=5)
```

---

## Memory Type Comparison Matrix

| Type | Capacity | Speed | Persistence | Best For |
|------|----------|-------|-------------|----------|
| **Short-Term** | Small (5-20) | ⚡⚡⚡ Fast | Session | Current task |
| **Long-Term** | Large (∞) | ⚡⚡ Medium | Permanent | History/learning |
| **Semantic** | Very Large | ⚡⚡ Medium | Permanent | Knowledge lookup |
| **Procedural** | Medium | ⚡⚡⚡ Fast | Permanent | Workflows |
| **Associative** | Medium-Large | ⚡⚡⚡ Fast | Permanent | Relationships |
| **Attention-Based** | Medium | ⚡⚡ Medium | Session | Relevance filtering |
| **Hierarchical** | Very Large | ⚡⚡ Medium | Permanent | Organized data |

---

## Integrated Memory Stack for VishAgent

```python
class VishAgentMemoryStack:
    def __init__(self):
        self.short_term = ShortTermMemory(max_size=20)
        self.long_term = LongTermMemory(db_connection)
        self.semantic = SemanticMemory(vector_store)
        self.procedural = ProceduralMemory()
        self.associative = AssociativeMemory()
        self.attention = AttentionMemory()
        self.hierarchical = HierarchicalMemory()
    
    async def process_claim(self, claim_request: Dict):
        # 1. Store in short-term for current processing
        self.short_term.add("user", f"Process claim: {claim_request['id']}")
        
        # 2. Retrieve relevant long-term history
        similar_claims = self.long_term.retrieve_similar_episodes(
            claim_request["description"]
        )
        
        # 3. Get semantic knowledge about policies
        policy_knowledge = self.semantic.retrieve_knowledge(
            "policy coverage rules"
        )
        
        # 4. Execute procedural workflow
        workflow_result = self.procedural.execute_procedure(
            "analyze_claim",
            claim_request
        )
        
        # 5. Find related entities
        related_entities = self.associative.retrieve_associations(
            claim_request["policy_id"],
            "covers"
        )
        
        # 6. Attend to most relevant information
        relevant_context = self.attention.attend(
            query=claim_request["description"],
            top_k=5
        )
        
        # 7. Store in hierarchical structure
        self.hierarchical.store_hierarchical(
            ["claims", "2024", claim_request["month"], claim_request["id"]],
            workflow_result
        )
        
        # 8. Store complete episode
        self.long_term.store_episode(
            session_id=claim_request["user_id"],
            episode={
                "messages": self.short_term.get_all(),
                "outcome": workflow_result["outcome"],
                "entities": related_entities
            }
        )
        
        return workflow_result
```

---

## Summary

Each memory type serves a specific purpose:

1. **Short-Term**: Fast, temporary context for current operations
2. **Long-Term**: Persistent storage for learning and history
3. **Semantic**: Knowledge base and conceptual understanding
4. **Procedural**: Learned workflows and processes
5. **Associative**: Entity relationships and connections
6. **Attention-Based**: Dynamic relevance and importance filtering
7. **Hierarchical**: Organized multi-level data storage

For optimal AI system performance, integrate all memory types to create a comprehensive memory stack that supports:
- Current task execution
- Historical learning
- Knowledge retrieval
- Workflow automation
- Relationship mapping
- Context prioritization
- Organized data management

---

**Last Updated:** January 15, 2026  
**Project:** VishAgent - MARVISH Industrial AI Assistant  
**Developer:** Vishnu Kiran M
 