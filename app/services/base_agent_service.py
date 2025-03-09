import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgentService:
    """Base class for agent search services that implement query decomposition and synthesis"""
    
    def _format_conversation_context(self, query, conversation_context):
        """Format the conversation context to provide to the agent"""
        if conversation_context and len(conversation_context) > 0:
            # Extract the most recent exchanges to inform the agent
            formatted_context = "Previous conversation:\n"
            for message in conversation_context[-3:]:  # Just use the last 3 messages for clarity
                role = message['role']
                if role != 'system':  # Skip system messages in the formatted context
                    formatted_context += f"{role.capitalize()}: {message['content']}\n"
            
            # Add an instruction for the agent
            return f"{formatted_context}\n\nConsidering the conversation above, answer this follow-up question: {query}"
        
        return query
    
    def _parse_subqueries(self, response):
        """Parse LLM response to extract subqueries"""
        subqueries = []
        for line in response.strip().split('\n'):
            # Remove bullet points and leading/trailing whitespace
            cleaned_line = re.sub(r'^\s*[-•*]\s*', '', line).strip()
            
            # Skip empty lines
            if cleaned_line:
                subqueries.append(cleaned_line)
        
        return subqueries
    
    def _decompose_query(self, query, is_web_search=False):
        """
        Decompose a complex query into multiple simpler subqueries
        
        Args:
            query (str): The original complex query
            is_web_search (bool): Whether this is for web search (affects prompt)
            
        Returns:
            list: List of subqueries
        """
        # Build the appropriate prompt based on whether it's web search or not
        if is_web_search:
            decompose_prompt = f"""
            You are an expert at breaking down complex questions into effective web search queries.
            
            Original Query: {query}
            
            Please break this query down into 2-4 specific, focused search queries that together will help answer the original question completely.
            Each search query should:
            1. Be phrased to maximize relevant search engine results
            2. Focus on a particular aspect of the original query
            3. Use search engine-friendly syntax (short, precise terms without unnecessary words)
            4. Avoid complex language that would reduce search effectiveness
            
            Format your response as a bulleted list with ONLY the search queries, nothing else.
            """
        else:
            decompose_prompt = f"""
            You are an expert at breaking down complex questions into simpler, more focused subqueries.
            
            Original Query: {query}
            
            Please break this query down into 2-4 specific, focused subqueries that together will help answer the original question completely.
            Each subquery should:
            1. Be self-contained and specific
            2. Focus on a particular aspect of the original query
            3. Be phrased as a complete question
            
            Format your response as a bulleted list with ONLY the subqueries, nothing else.
            """
        
        # Generate the decomposition
        response = self.llm_service.generate_response(
            prompt=decompose_prompt,
            context=None,
            max_tokens=500
        )
        
        # Parse the subqueries
        subqueries = self._parse_subqueries(response)
        
        # If no subqueries were extracted or the LLM failed, return the original query
        if not subqueries:
            logger.warning("Failed to decompose query, using original query")
            return [query]
        
        return subqueries
    
    def _decompose_query_informed(self, query, initial_response, initial_contexts, is_web_search=False):
        """
        Decompose a query using context from initial results
        
        Args:
            query (str): The original complex query
            initial_response (str): The response from initial search
            initial_contexts (list): The contexts retrieved in the initial search
            is_web_search (bool): Whether this is for web search (affects prompt)
            
        Returns:
            list: List of subqueries
        """
        # Format contexts for the decomposition prompt
        formatted_contexts = ""
        for i, context in enumerate(initial_contexts[:3]):  # Limit to first 3 contexts
            formatted_contexts += f"Context {i+1}: {context.get('content', '')}\n"
            formatted_contexts += f"Source: {context.get('document_title', 'Unknown')}\n\n"
        
        # Build the appropriate prompt based on whether it's web search or not
        search_type = "web search" if is_web_search else "search"
        query_type = "search queries" if is_web_search else "questions"
        
        decompose_prompt = f"""
        You are an expert at breaking down complex questions into effective {query_type}.
        
        Original Query: {query}
        
        I've already done an initial {search_type} and found some information, but we need to explore further:
        
        Initial Results: 
        {formatted_contexts}
        
        Based on what we've found so far, please identify 2-3 specific, focused follow-up {query_type} that would help us:
        1. Fill in important missing information not covered in the initial search
        2. Explore specific aspects of the query that weren't fully addressed
        3. Resolve any ambiguities or contradictions in the initial results
        
        Each query should:
        - Be focused on gathering new information not already covered
        - NOT duplicate information we already have from the initial search
        """
        
        if is_web_search:
            decompose_prompt += """
        - Be phrased to maximize relevant search engine results
        - Use search engine-friendly syntax (short, precise terms without unnecessary words)
            """
        else:
            decompose_prompt += """
        - Be self-contained and specific
        - Be phrased as a complete question
            """
        
        decompose_prompt += """
        Format your response as a bulleted list with ONLY the queries, nothing else.
        """
        
        # Generate the decomposition
        response = self.llm_service.generate_response(
            prompt=decompose_prompt,
            context=None,
            max_tokens=500
        )
        
        # Parse the subqueries
        subqueries = self._parse_subqueries(response)
        
        # If no subqueries were extracted or the LLM failed, return default follow-ups
        if not subqueries:
            logger.warning(f"Failed to decompose query using informed strategy, using default follow-up queries")
            if is_web_search:
                subqueries = [
                    f"{query} latest information",
                    f"{query} alternative perspectives"
                ]
            else:
                subqueries = [
                    f"What additional details can be found about {query}?",
                    f"Are there any alternative perspectives on {query}?"
                ]
        
        return subqueries
    
    def _synthesize_answer(self, original_query, intermediate_results, is_web_search=False):
        """
        Synthesize a comprehensive answer from intermediate results
        
        Args:
            original_query (str): The original user query
            intermediate_results (list): List of dictionaries with subquery results
            is_web_search (bool): Whether this is for web search synthesis
            
        Returns:
            str: Synthesized comprehensive answer
        """
        # Format intermediate results for the synthesis prompt
        formatted_results = ""
        for i, result in enumerate(intermediate_results):
            query_type = "Search Query" if is_web_search else "Subquery"
            formatted_results += f"{query_type} {i+1}: {result['subquery']}\n"
            formatted_results += f"Results: {result['answer']}\n\n"
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        You are tasked with synthesizing a comprehensive answer to a complex query based on search results.
        
        Original Query: {original_query}
        
        I've broken this query down and found results for each part:
        
        {formatted_results}
        
        Please synthesize a comprehensive, cohesive answer to the original query that:
        1. Directly addresses the original question
        2. Integrates information from all results
        3. Presents a logical flow of information
        4. Avoids unnecessary repetition
        5. Maintains factual accuracy from the source information
        """
        
        if is_web_search:
            synthesis_prompt += """
        6. Includes proper citations to web sources including URLs in parentheses
        7. Notes any conflicting information found and provides a balanced perspective
        
        Your answer should be thorough but concise, well-structured, and directly useful to the person who asked the original query.
        Be careful to only include factual information from the search results, and acknowledge any significant information gaps.
        """
        else:
            synthesis_prompt += """
        6. Citing references to the source documents where applicable with all relevant document_title.
        7. If the results do not contain sufficient or relevant details, don't answer and state there is no relevant context.
        
        Your answer should be thorough but concise, well-structured, and directly useful to the person who asked the original query.
        """
        
        # Generate synthesized response
        synthesized_answer = self.llm_service.generate_response(
            prompt=synthesis_prompt,
            context=None,
            max_tokens=1000
        )
        
        return synthesized_answer