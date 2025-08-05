HEAD
# Data-Visualization-and-Story-Telling-with-AI

# 1. Introduction

In an era of ubiquitous artificial intelligence, I leverage AI and large language models (LLMs) as
pedagogical tools to deepen student learning. In my undergraduate course Data Visualization and
Storytelling with AI, students learn core visualization principles, modern web development,
and hardware integration while collaborating with AI assistants. The overarching goal is to
empower students as critical thinkers who can harness LLMs for ideation, coding, and analysis,
rather than using them as “oracles”. This integration is driven by a clear rationale: by offloading
boilerplate coding tasks and offering on-demand guidance, AI tools lower barriers for students
(even those with no programming background) to engage in real-world data projects. The emphasis
remains on understanding, iteration, and explanation over mere polished outputs. In practice,
this means students are taught to design effective prompts and to verify every AI-generated result,
aligning with a stated learning outcome that they “refine prompts to obtain, debug, and explain
R code from LLMs, validating outputs critically”. Such an approach not only keeps the human
in control of the problem-solving process but also instills responsible technology use by requiring
transparent documentation and skepticism of AI outputs. Overall, the pedagogical strategy positions
AI as a catalyst for deeper learning: students tackle complex, authentic projects with AI
support, developing both technical skills and the judgment to use these tools ethically in today’s
data-driven world.

**1.1 Instructional Strategies**
The course is structured around a series of LLM-integrated case studies and projects that progressively
build student skills. Each case study introduces realistic datasets or scenarios and requires
students to use prompt engineering and AI-assisted coding in service of clear learning objectives.
Crucially, every use of an AI tool is coupled with careful

**1.1.1 Case Study 1: Visualization Critique**
Students analyze complete and flawed charts. They prompt LLMs to “List three misleading aspects
and suggest improved labels”, then critically assess those suggestions. This trains prompt clarity and
visual literacy: AI sparks deeper observation, while students confirm and refine design principles.

**1.1.2 Case Study 2: Data Analysis with R**
Working on a used-car dataset, students craft prompts for R code (e.g. ggplot2 pipelines) and
iteratively refine model output. Each AI-generated snippet is unit-tested and debugged by the
student, reinforcing understanding of R syntax, data structures, and statistical reasoning. Grading
rewards the documented process—prompt, test, revise—not just the final visualization.

**1.1.3 Case Study 3: IoT Sensor Project**
Learners assemble a Raspberry Pi with DHT22 sensors to collect environmental data. They use
LLMs for Python setup scripts and wiring guidance, then validate every step through device testing.
For bias identification, AI suggests color palettes and annotation strategies, which students evaluate
and correct, gaining hands-on experience in ethical data storytelling.

**1.1.4Case Study 4: Interactive Web Dashboard**
Students build React dashboards with Recharts and PapaParse. They prompt LLMs for code to
fetch and parse CSV data, manage state (e.g. using useMemo), and render charts. Each integration is
verified by comparing rendered visuals against console-logged data, teaching both web development
and fidelity in data representation.

**1.1.5Prompt Engineering Portfolio**
Throughout, students maintain a portfolio logging original prompts, raw outputs, modifications,
and verification steps. This reflective tool documents learning moments—both AI successes and
“hallucinations”—and is assessed as a core deliverable, reinforcing iterative refinement and skepticism.

**1.1.6Mini-Project and Capstone**
The mini-project challenges students to critique real-world visualizations using AI brainstorming
while documenting corrections. The capstone synthesizes hardware, software, and web development:
students collect sensor data, scaffold dashboards with LLM assistance, and draft narrative
reports—each AI-assisted step meticulously verified. This end-to-end workflow exemplifies how AI
accelerates complex projects without sacrificing rigor.

# 2. Student Outcomes and Engagement

**2.1 Debugging Autonomy**
By engaging in ask–evaluate–refine loops with AI, students become self-sufficient debuggers. They
learn to formulate diagnostic prompts, interpret AI suggestions, and validate fixes, moving from
passive code consumers to active problem solvers.

**2.2 Reflective Learning**
Prompt logs transform tacit insights into explicit reflections. Students describe how AI helped
them discover new functions (e.g. geom smooth), catch model errors, and solidify conceptual understanding—
leading to measurable gains in statistical reasoning and bias detection.

**2.3 Motivation and Ownership**
Authentic, real-world tasks—augmented by an AI “teammate”—heighten engagement. Learners
pursue creative extensions, document AI interaction stories, and proudly share their interactive
dashboards, demonstrating both technical skill and critical oversight.

# Conclusion
Integrating AI and LLMs in DAT-230 enriches the learning experience by coupling rapid prototyping
with strict verification and transparent documentation. Students emerge not only with proficiency
in R, React, and hardware integration, but with critical thinking skills and ethical awareness
necessary for responsible AI use. This AI-augmented pedagogy exemplifies how modern tools
can elevate undergraduate education, preparing graduates to harness technology creatively and
conscientiously.



=======
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
>>>>>>> 927b380 (Initialize project using Create React App)
