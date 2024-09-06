import asyncio
import json
import random
import ssl
import aiohttp
import time
import numpy as np
from tqdm import tqdm

# API endpoint
api_url = "https://mock_c5eb6522932040cfb124aecf3a8e7578.mock.insomnia.rest/opus-mt"
# api_url = "https://ray-server.sigma-cd3.aws.itsma-ng.net/opus-mt-en-zh"

# Test data
test_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "This is a test sentence.",
    "Artificial intelligence is transforming industries.",
    "How are you today?",
    "FastAPI is a modern, fast web framework for building APIs with Python.",
]

# test_sentences = [
#     "As technology continues to evolve at an unprecedented pace, the integration of artificial intelligence and machine learning into everyday applications is reshaping industries ranging from healthcare and finance to education and entertainment, fostering a new era of innovation and growth.",
#     "Climate change, driven by the rising levels of greenhouse gases in the atmosphere, poses an increasingly dire threat to ecosystems, biodiversity, and human communities, necessitating swift and coordinated global action to mitigate its impact and transition to a more sustainable future.",
#     "The human brain, with its vast network of neurons and synapses, is one of the most complex and enigmatic structures in the universe, capable of remarkable feats of memory, cognition, and creativity, yet still largely misunderstood by the scientific community.",
#     "Globalization has facilitated the unprecedented movement of goods, services, and capital across borders, creating new opportunities for economic growth and development, while also exacerbating inequalities and contributing to the rise of populism and protectionist sentiments in many parts of the world.",
#     "The concept of free will has been debated by philosophers for centuries, with some arguing that humans possess the ability to make choices independent of external determinants, while others contend that every decision is the inevitable consequence of preceding causes and conditions.",
#     "In George Orwell's dystopian novel '1984', the totalitarian regime, led by the enigmatic figure of Big Brother, uses surveillance, propaganda, and psychological manipulation to control every aspect of the citizens' lives, creating a chilling vision of a world devoid of freedom and individuality.",
#     "The fall of the Roman Empire, often attributed to a combination of internal decay, external pressures from barbarian invasions, and economic instability, marked a profound transformation in the political and cultural landscape of Europe, paving the way for the emergence of the Middle Ages.",
#     "Advances in medical science, particularly in the fields of genomics and personalized medicine, are enabling healthcare providers to develop more targeted and effective treatments for a wide range of diseases, offering new hope to patients suffering from conditions that were once considered untreatable.",
#     "Cognitive behavioral therapy, a widely used and empirically supported treatment modality, focuses on helping individuals identify and challenge distorted thinking patterns and maladaptive behaviors in order to develop healthier coping mechanisms and improve overall mental well-being.",
#     "The future of education is likely to be shaped by the increasing use of digital technologies, including online learning platforms, artificial intelligence, and virtual reality, which have the potential to revolutionize the way students access information, interact with instructors, and collaborate with peers.",
#     "The rapid urbanization of cities around the world has led to significant challenges in terms of infrastructure, transportation, and housing, requiring innovative solutions to ensure that urban environments remain sustainable and livable for future generations.",
#     "The advent of social media has transformed the way people communicate, providing a platform for real-time interaction and information sharing, while also raising concerns about privacy, misinformation, and the erosion of meaningful human connections.",
#     "Quantum computing, which harnesses the principles of quantum mechanics to process information in ways that classical computers cannot, promises to revolutionize fields such as cryptography, materials science, and drug discovery, though significant technical challenges remain.",
#     "The rise of renewable energy sources, such as solar and wind power, represents a critical step toward reducing humanity's reliance on fossil fuels, but challenges related to energy storage and grid integration must be overcome to fully realize their potential.",
#     "Artificial intelligence, particularly in the form of natural language processing and machine learning algorithms, has the potential to automate many routine tasks, increasing efficiency while also raising ethical questions about the impact on employment and decision-making processes.",
#     "The exploration of space, once limited to government agencies and large institutions, has increasingly become a domain for private companies, opening up new possibilities for commercial ventures, scientific research, and even space tourism.",
#     "The spread of infectious diseases, such as COVID-19, highlights the interconnectedness of the modern world and underscores the importance of global cooperation in monitoring, controlling, and responding to health crises that transcend national borders.",
#     "The development of autonomous vehicles, which rely on a combination of sensors, machine learning, and complex algorithms, has the potential to reshape transportation systems, reducing accidents and traffic congestion while raising concerns about safety, regulation, and ethical considerations.",
#     "The human genome project, which mapped the entire sequence of human DNA, has opened up new frontiers in medical research, allowing scientists to better understand genetic predispositions to diseases and develop personalized treatments based on an individual's genetic profile.",
#     "The widespread adoption of 5G technology, which promises faster internet speeds and more reliable connections, is expected to fuel innovations in industries ranging from telemedicine and remote work to smart cities and the Internet of Things.",
#     "The role of education in promoting social mobility and reducing inequality has long been recognized, but disparities in access to quality education, particularly in marginalized communities, remain a significant barrier to achieving true equality of opportunity.",
#     "The relationship between mental health and physical health is increasingly being understood as interconnected, with stress, anxiety, and depression known to have tangible effects on the body, while physical ailments can exacerbate mental health challenges.",
#     "Renewable energy technologies have advanced significantly in recent years, making solar panels, wind turbines, and battery storage systems more efficient and affordable, but widespread adoption is still hindered by policy barriers, grid challenges, and economic considerations.",
#     "The history of human civilization is marked by periods of tremendous technological progress, from the invention of the wheel and the printing press to the Industrial Revolution and the digital age, each of which has fundamentally transformed the way people live, work, and interact.",
#     "The application of machine learning in healthcare, particularly in diagnostic imaging, has the potential to vastly improve the accuracy and speed of diagnoses, though ethical concerns about data privacy and algorithmic bias must be carefully addressed.",
#     "The increasing prevalence of mental health disorders in the modern world has prompted a re-evaluation of how societies approach well-being, leading to greater emphasis on early intervention, holistic care, and the destigmatization of seeking help for mental health issues.",
#     "Blockchain technology, originally developed to support cryptocurrencies like Bitcoin, is now being explored for a wide range of applications, from supply chain management and voting systems to secure data sharing and intellectual property protection.",
#     "The economic impact of the COVID-19 pandemic has been profound, leading to widespread job losses, business closures, and significant disruptions to global supply chains, while also accelerating trends toward remote work, e-commerce, and digital transformation.",
#     "Advances in artificial intelligence and robotics are leading to the development of machines capable of performing tasks that were once the exclusive domain of humans, raising fundamental questions about the future of work and the role of technology in society.",
#     "The process of globalization, while offering opportunities for economic growth and cultural exchange, has also led to the homogenization of local cultures, the erosion of traditional practices, and the rise of tensions related to identity and sovereignty.",
#     "The study of ancient civilizations, through the examination of archaeological sites and artifacts, provides invaluable insights into the social, political, and economic structures of the past, shedding light on the achievements and challenges of societies long gone.",
#     "The digital revolution has transformed the way information is produced, distributed, and consumed, creating new opportunities for knowledge sharing while also raising concerns about misinformation, digital divides, and the commodification of data.",
#     "The role of government in regulating emerging technologies, such as artificial intelligence and biotechnology, is increasingly being debated, with some advocating for a hands-off approach to encourage innovation, while others call for stricter oversight to ensure public safety and ethical standards.",
#     "The potential of gene editing technologies, such as CRISPR, to revolutionize medicine and agriculture is immense, offering the ability to cure genetic diseases and enhance crop yields, but ethical questions about the implications of altering the genetic code of organisms remain unresolved.",
#     "The long-term effects of climate change on biodiversity, food security, and human health are still being studied, but it is clear that rising temperatures, changing precipitation patterns, and more frequent extreme weather events will have far-reaching consequences.",
#     "The rise of digital currencies, including cryptocurrencies and central bank digital currencies, is reshaping the global financial system, offering new opportunities for innovation in payments and finance, while also presenting regulatory challenges and risks related to security and volatility.",
#     "The future of work is likely to be shaped by the continued integration of technology into the workplace, with automation, artificial intelligence, and remote work transforming traditional job roles and creating new opportunities and challenges for workers and employers alike.",
#     "The ethical implications of artificial intelligence, particularly in areas such as surveillance, decision-making, and personal privacy, are increasingly being scrutinized, with calls for the development of guidelines and regulations to ensure that AI technologies are used responsibly.",
#     "The development of electric vehicles, along with advancements in battery technology, is key to reducing greenhouse gas emissions from the transportation sector, but widespread adoption will require significant investments in charging infrastructure and changes to consumer behavior.",
#     "The exploration of the deep ocean, much like the exploration of space, represents one of the last frontiers of scientific discovery, with vast areas of the seafloor still unmapped and many species yet to be discovered, despite advances in underwater technology.",
#     "The social and political upheavals of the 21st century, from the Arab Spring to the rise of populist movements in Europe and the Americas, have raised questions about the resilience of democratic institutions and the role of technology in shaping public opinion and governance.",
#     "The use of artificial intelligence in creative fields, such as music, art, and literature, is pushing the boundaries of what machines are capable of, leading to new forms of expression and collaboration between humans and machines, while also challenging traditional notions of creativity.",
#     "The study of consciousness, one of the most profound and elusive topics in philosophy and neuroscience, seeks to understand the nature of subjective experience, raising fundamental questions about the mind, the self, and the relationship between the brain and consciousness.",
#     "The impact of climate change on the global food system is a growing concern, with rising temperatures, changing precipitation patterns, and more frequent extreme weather events threatening to disrupt agricultural production and exacerbate food insecurity in vulnerable regions.",
#     "The rise of authoritarianism in some parts of the world, coupled with the erosion of democratic norms in others, has sparked renewed interest in the study of political systems and the factors that contribute to the stability or collapse of governments.",
#     "The rapid pace of technological innovation, particularly in areas such as artificial intelligence, biotechnology, and renewable energy, is transforming industries and societies at an unprecedented rate, offering both opportunities for growth and challenges related to ethics, regulation, and inequality.",
#     "The role of storytelling in human culture is ancient and enduring, serving as a means of passing down knowledge, preserving traditions, and shaping collective identities, while also evolving with new technologies, from the printing press to digital media.",
#     "The evolution of human language, from the development of early forms of communication to the complexity of modern languages, is a testament to the adaptability and creativity of the human mind, with linguists continuing to study the origins, structure, and diversity of languages around the world.",
#     "The intersection of science and ethics is increasingly coming to the forefront as advances in fields such as genetics, artificial intelligence, and environmental science challenge traditional moral frameworks and require new ways of thinking about responsibility, justice, and human flourishing."
# ]

# Benchmark settings
num_requests = 40  # Number of requests to simulate
request_rate = 20  # Requests per second (simulated load)

# Store response times
response_times = []

# Create SSL context with verification disabled
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def send_request(session, text):
    req_body = {
        "inputs": [
            ">>cmn_Hans<<{}".format(text)
        ]
    }

    start_time = time.time()
    async with session.post(api_url, json=req_body, ssl=ssl_context) as response:
        result = await response.json()
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Response body: {result}, Response Time: {response_time:.4f} seconds")
        return response_time


async def benchmark():
    global response_times
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        for _ in tqdm(range(num_requests // request_rate)):
            tasks = []  # 存储任务

            # Get a batch of sentences to send to the API
            random.shuffle(test_sentences)
            texts = [test_sentences[i % len(test_sentences)] for i in range(request_rate)]

            for text in texts:
                # 将每个请求添加到任务列表
                task = send_request(session, text)
                tasks.append(task)
            response_times_iteration = await asyncio.gather(*tasks)
            response_times = response_times + response_times_iteration

            # Sample the request interval from the exponential distribution.
            interval = np.random.exponential(1.0 / request_rate)
            # The next request will be sent after the interval.
            await asyncio.sleep(interval)

        # 使用 asyncio.gather 并发执行所有任务
        # response_times = await asyncio.gather(*tasks)
    # response_times.insert(response_times_iteration)
    return time.time() - start_time


# Run the benchmark
total_time = asyncio.run(benchmark())

# Calculate metrics
throughput = num_requests / total_time

# Calculate percentiles
p95 = np.percentile(response_times, 95)
p99 = np.percentile(response_times, 99)

print("======================== Benchmark Results =======================")
print(f"Total duration: {total_time:.2f} seconds")
print(f"Number of requests: {num_requests}")
print(f"Request rate: {request_rate} requests per second")
print(f"Throughput: {throughput:.2f} requests/second")
print(f"Response Time P95: {p95:.4f} seconds")
print(f"Response Time P99: {p99:.4f} seconds")
