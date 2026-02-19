# Style Vault

This file contains examples of Instagram posts that serve as style references for the content creation agents. Each post is enclosed in `<post>` tags and includes metadata about the topic, style, and target audience.

Use these examples to understand the desired tone, structure, formatting, and presentation style for Instagram carousel posts.

---

## Example Posts

<post id="random-forests-example" topic="Random Forests" style="educational-technical" slides="9">

### Slide 1
**Title:** Random Forests  
**Content:**  
@learningalgorithm  
Why do Random Forests perform better than decision trees?

**Layout:** Title prominently displayed, question as hook, handle at bottom

---

### Slide 2
**Title:** Decision Trees  
**Content:**  
@learningalgorithm  
A decision tree recursively splits data to build a tree by selecting the most informative feature at each node.  
The greedy nature of the splits makes early decisions irreversible, leading to over-fitting.

**Layout:** Title at top, technical explanation in center, handle at bottom

---

### Slide 3
**Title:** Voting using Multiple Trees  
**Content:**  
The solution proposed to the problem was to train multiple decision trees (say 50) and have them all make predictions.  
We would then consider the result given by a majority of trees as the correct prediction. This is an ensemble approach  
@learningalgorithm

**Layout:** Title, clear explanation of solution, handle at bottom

---

### Slide 4
**Title:** Feature Randomness  
**Content:**  
This is a point where we want to deviate from a traditional decision tree  
Instead of considering all features at every SPLIT, we want to only consider a random subset of features at every split  
Remember: Each tree is NOT built on random features — instead, EVERY SPLIT in EVERY TREE considers random features.  
@learningalgorithm

**Layout:** Title, bold emphasis on key distinction, handle at bottom

---

### Slide 5
**Title:** Voting Process  
**Content:**  
For classification, we make every tree make predictions. Then, we take the prediction made by the majority of trees as the output  
For regression, we simply average the predictions made by all the trees  
@learningalgorithm

**Layout:** Title, practical explanation with classification vs regression, handle at bottom

---

### Slide 6
**Title:** Overall Algorithm - Random Forest  
**Content:**  
Build decision trees such that each node looks at a random subset of features  
Grow deep trees till a criterion (e.g. each leaf node must have 5–20 points) is met.  
Take a majority vote or average the predictions  
@learningalgorithm

**Layout:** Title, step-by-step algorithm, handle at bottom

---

### Slide 7
**Title:** Advantages of Random Forest  
**Content:**  
The key advantage of Random forests is that they rarely over-fit.  
The averaging process of randomized trees stabilizes the predictions.  
Another advantage is that they can be trained in parallel — i.e. each tree in a random forest is trained independently of others.  
Thus, parallel processing can be exploited.  
@learningalgorithm

**Layout:** Title, bullet-style advantages list, handle at bottom

---

### Slide 8
**Title:** Why do they perform better than decision trees?  
**Content:**  
Because of averaging and randomization.  
Averaging reduces over-fitting (which is a key issue with decision trees) and randomized splits cause the individual trees to become more independent  
@learningalgorithm

**Layout:** Title as question, concise answer with explanation, handle at bottom

---

### Slide 9
**Title:** Engagement  
**Content:**  
Let me know in the comments which other algorithms I should cover  
@learningalgorithm

**Layout:** Call-to-action, handle at bottom

</post>

---

<post id="neural-networks-example" topic="Neural Networks" style="educational-visual" slides="8">

### Slide 1
**Title:** Neural Networks Explained  
**Content:**  
@learningalgorithm  
How do neural networks actually learn?

**Layout:** Bold title, engaging question, handle placement

---

### Slide 2
**Title:** Definition  
**Content:**  
A **Neural Network** is a computational model inspired by biological neurons that learns patterns from data through layers of interconnected nodes.  
Each connection has a **weight** that gets adjusted during training.  
@learningalgorithm

**Layout:** Title, definition with bold key terms, handle at bottom

---

### Slide 3
**Title:** Architecture  
**Content:**  
Input Layer → Hidden Layers → Output Layer  
Each layer transforms the data, extracting increasingly complex features.  
The **depth** of the network (number of layers) determines its capacity to learn complex patterns.  
@learningalgorithm

**Layout:** Visual flow representation, explanation of layers, handle at bottom

---

### Slide 4
**Title:** Forward Propagation  
**Content:**  
Data flows forward through the network:  
1. Multiply inputs by weights  
2. Add bias terms  
3. Apply activation function  
4. Pass to next layer  
Formula: `output = activation(weights × input + bias)`  
@learningalgorithm

**Layout:** Title, numbered steps, simple formula, handle at bottom

---

### Slide 5
**Title:** Activation Functions  
**Content:**  
**ReLU**: max(0, x) - Most common, fast to compute  
**Sigmoid**: 1/(1+e^-x) - Output between 0 and 1  
**Tanh**: (e^x - e^-x)/(e^x + e^-x) - Output between -1 and 1  
Activation functions introduce **non-linearity** into the network.  
@learningalgorithm

**Layout:** Title, formatted list with formulas, key insight in bold, handle at bottom

---

### Slide 6
**Title:** Backpropagation  
**Content:**  
The learning algorithm:  
1. Calculate error at output  
2. Propagate error backwards  
3. Compute gradients using chain rule  
4. Update weights using gradient descent  
This is how the network "learns" from mistakes.  
@learningalgorithm

**Layout:** Title, step-by-step process, key insight, handle at bottom

---

### Slide 7
**Title:** Why They Work  
**Content:**  
**Universal Approximation Theorem**: A neural network with enough hidden units can approximate any continuous function.  
The combination of layers, non-linear activations, and iterative learning creates a powerful learning system.  
@learningalgorithm

**Layout:** Title, theorem highlighted, practical implication, handle at bottom

---

### Slide 8
**Title:** Your Turn  
**Content:**  
What aspect of neural networks should I explain next?  
Comment: Optimization, Regularization, or Architectures  
@learningalgorithm

**Layout:** Call-to-action with specific options, handle at bottom

</post>

---

## Style Guidelines Extracted from Examples

### Content Structure
- **Slide 1**: Hook with engaging question about the topic
- **Slide 2**: Clear definition with **bold** key terms
- **Middle Slides**: Technical details, algorithms, comparisons, advantages
- **Penultimate Slide**: Summary or key insight
- **Final Slide**: Call-to-action for engagement

### Formatting
- Always include `@learningalgorithm` on every slide
- Use **bold** for key terms and concepts
- Keep content concise and focused
- Use numbered lists for processes/algorithms
- Include simple formulas where relevant

### Tone
- Educational but not condescending
- Technical but accessible
- Focused on intermediate concepts
- Practical and application-oriented
- Clear explanations without jargon overload

### Layout Descriptions
- Title at top
- Content in center or structured format
- Handle at bottom
- Visual flow for processes (using arrows: →)
- Formula highlighting when applicable

---

## Adding Your Own Examples

To add a new example post to this style vault, use the following format:

```markdown
<post id="unique-id" topic="Topic Name" style="style-type" slides="number">

### Slide 1
**Title:** [Slide Title]
**Content:**  
[Slide content with @learningalgorithm]

**Layout:** [Layout description]

---

### Slide 2
...

</post>
```

**Metadata attributes:**
- `id`: Unique identifier for the post
- `topic`: The main topic covered
- `style`: Type of post (educational-technical, educational-visual, comparison, tutorial, etc.)
- `slides`: Number of slides in the carousel

---

**Note:** This style vault helps maintain consistency across posts and provides concrete examples for the AI agents to reference when creating new content.
