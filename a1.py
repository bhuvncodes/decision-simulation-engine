import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import openai
from dotenv import load_dotenv

# Load env variables automatically from .env (good for hackathon portability)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-here")

# Configure OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_ai_response(prompt):
    """Get AI response in JSON format"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a startup mentor and simulation engine. Always respond in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {}

def fallback_decisions(startup_data):
    """A fallback decision set so the app never feels empty during a hackathon demo."""
    stage = startup_data.get('stage', 'idea').lower()
    if stage == 'idea':
        return [
            {"title": "Validate problem with early users",
             "description": "Run interviews and small surveys to confirm the pain point before building.",
             "options": ["Conduct 15 customer interviews", "Launch a landing page for signups", "Run a quick paid ad test"],
             "stakeholders": ["customers", "team", "investors"]},
            {"title": "Choose a revenue model",
             "description": "Decide how the startup will earn money from day one.",
             "options": ["Freemium with premium upgrade", "Transaction fee model", "Subscription pre-sale"],
             "stakeholders": ["customers", "investors", "partners"]},
            {"title": "Build MVP priority",
             "description": "Pick the first features that demonstrate value quickly.",
             "options": ["Core workflow first", "Analytics dashboard", "Integration with top platform"],
             "stakeholders": ["team", "customers"]},
            {"title": "Create a go-to-market launch plan",
             "description": "Decide the initial GTM strategy for first traction.",
             "options": ["Community and content marketing", "Influencer partnerships", "Direct sales to pilot customers"],
             "stakeholders": ["customers", "partners", "team"]},
            {"title": "Set milestone-based investor story",
             "description": "Define the mini milestones that impress early investors.",
             "options": ["Hit 100 signups in 30 days", "Secure 3 pilot customers", "Close first revenue in Q1"],
             "stakeholders": ["investors", "team"]}
        ]
    else:
        return [
            {"title": "Optimize initial onboarding conversion",
             "description": "Reduce friction so early users complete full signup quickly.",
             "options": ["Simplify signup flow", "Add interactive walkthrough", "Offer sign-up incentives"],
             "stakeholders": ["customers", "team"]},
            {"title": "Define early pricing test",
             "description": "Test pricing tiers to find product-market-price fit.",
             "options": ["Introductory discounted subscription", "Usage-based billing", "Fixed direct price"],
             "stakeholders": ["customers", "investors", "partners"]},
            {"title": "Choose scaling path",
             "description": "Select initial scaling lever for the prototype phase.",
             "options": ["Platform integration", "Channel partner network", "Paid growth campaigns"],
             "stakeholders": ["partners", "team"]},
            {"title": "Gather quantifiable user feedback",
             "description": "Get numbers from 100 users to prioritize features accurately.",
             "options": ["NPS survey", "Feature voting board", "A/B test onboarding"],
             "stakeholders": ["customers", "team"]},
            {"title": "Build investor runway scenario",
             "description": "Create a financial model for 12-month runway before scaling.",
             "options": ["Lean expenses + strong revenues", "Growth-first burn strategy", "Strategic partnership funding"],
             "stakeholders": ["investors", "team"]}
        ]


def generate_decisions(startup_data):
    """Generate 3-5 decision points based on startup stage and idea"""
    stage = startup_data.get('stage', 'idea')
    idea = startup_data.get('idea', '')
    users = startup_data.get('users', '')
    preset = startup_data.get('preset', 'general')

    prompt = f"""
    Generate exactly 5 key decision points for an early-stage startup at {stage.upper()} stage.
    Startup: {startup_data.get('name')}
    Idea: {idea}
    Target Users: {users}
    Preferred hackathon mode: {preset}

    For each decision, provide:
    - title: The decision to make
    - description: Context for this decision
    - options: Array of 3-4 realistic options (strings)
    - stakeholders: Array of affected stakeholder groups (customers, investors, team, partners, community)

    Return as JSON with structure:
    {{
        "decisions": [
            {{"title": "", "description": "", "options": [], "stakeholders": []}},
            ...
        ]
    }}
    """

    try:
        response = get_ai_response(prompt)
        decisions = response.get('decisions', [])
        if not decisions:
            # Fallback in the rare case of AI fail
            decisions = fallback_decisions(startup_data)
    except Exception:
        decisions = fallback_decisions(startup_data)

    return decisions


def get_decision_outcomes(startup_data, decision, choice):
    """Get stakeholder reactions and metric impacts for a chosen decision"""
    prompt = f"""
    A user is making a business decision in their startup simulation. Analyze the decision impact.
    
    Startup: {startup_data.get('name')}
    Stage: {startup_data.get('stage')}
    Idea: {startup_data.get('idea')}
    Decision Title: {decision.get('title')}
    Their Choice: {choice}
    Affected Stakeholders: {', '.join(decision.get('stakeholders', []))}
    
    Provide analysis as JSON with:
    - insight: Brief explanation of why this is a good/risky choice
    - suggestion: Alternative approach or improvement
    - stakeholder_reactions: Object with each stakeholder group -> "positive"/"negative"/"neutral"
    - metric_changes: Object with {{"impact": -5 to 5, "finance": -5 to 5, "risk": -5 to 5, "trust": -5 to 5}}
    - score_change: Overall score impact (-10 to 10)
    - competitor_reaction: Why competitors may respond to this decision
    - risk_matrix_insight: High-level mapping of market/product/team/regulatory risk
    
    Return as JSON.
    """
    
    response = get_ai_response(prompt)
    if not response:
        # fallback safe defaults if API fails
        response = {
            'insight': 'This choice is reasonable with moderate risk and strategic value.',
            'suggestion': 'Consider validating quickly and tracking early metrics.',
            'stakeholder_reactions': {s:'neutral' for s in decision.get('stakeholders', [])},
            'metric_changes': {'impact': 0, 'finance': 0, 'risk': 0, 'trust': 0},
            'score_change': 0,
            'competitor_reaction': 'Competitors may respond with better pricing or feature focus.',
            'risk_matrix_insight': 'Market and product risks are moderate; focus on execution.'
        }
    return response


def generate_competitor_analysis(startup_data):
    """Create a quick competition view from the startup idea."""
    idea = startup_data.get('idea', '')
    prompt = f"""
    The startup idea: {idea}
    Provide a competitor snapshot with 3 likely competitors, each including:
    - name
    - key differentiation
    - risk/opportunity
    - recommended counter strategy
    Return JSON: {{"competitors":[{{...}}]}}
    """
    response = get_ai_response(prompt)
    competitors = response.get('competitors') if response else None
    if not competitors:
        competitors = [
            {'name': 'Competitor A', 'differentiation': 'Price leader', 'risk_opportunity': 'High price pressure', 'counter': 'Focus on niche use case'},
            {'name': 'Competitor B', 'differentiation': 'Feature-rich', 'risk_opportunity': 'Complex product', 'counter': 'Simplify onboarding'},
            {'name': 'Competitor C', 'differentiation': 'Enterprise focus', 'risk_opportunity': 'Long sales cycles', 'counter': 'Target SMB first'}
        ]
    return competitors


def build_risk_matrix(metrics):
    """Produce a risk matrix from current metrics."""
    return {
        'market': 'High' if metrics['impact'] < 40 else 'Medium' if metrics['impact'] < 70 else 'Low',
        'finance': 'High' if metrics['finance'] < 40 else 'Medium' if metrics['finance'] < 70 else 'Low',
        'execution': 'High' if metrics['trust'] < 40 else 'Medium' if metrics['trust'] < 70 else 'Low',
        'strategy': 'High' if metrics['risk'] > 70 else 'Medium' if metrics['risk'] > 40 else 'Low'
    }


def project_kpis(metrics):
    """Project simple KPI curves for the next 3 quarters"""
    return {
        'q1': {'impact': min(100, metrics['impact'] + 5), 'finance': min(100, metrics['finance'] + 4), 'risk': max(0, metrics['risk'] - 2), 'trust': min(100, metrics['trust'] + 3)},
        'q2': {'impact': min(100, metrics['impact'] + 10), 'finance': min(100, metrics['finance'] + 8), 'risk': max(0, metrics['risk'] - 5), 'trust': min(100, metrics['trust'] + 6)},
        'q3': {'impact': min(100, metrics['impact'] + 18), 'finance': min(100, metrics['finance'] + 14), 'risk': max(0, metrics['risk'] - 8), 'trust': min(100, metrics['trust'] + 11)}
    }

def generate_competitor_reactions(decision_choice, competitors):
    """Generate AI-driven competitive counter-reactions to player decision"""
    prompt = f"""
    Player's decision choice: {decision_choice}
    Competitors facing this move: {json.dumps(competitors, indent=2)}
    
    Generate realistic competitive counter-moves for this player action.
    Return JSON with:
    - reactions: Array of 3 competitor reaction objects, each with: name, counter_move, reasoning
    - market_shift: Brief market impact analysis
    
    Focus on business realism and strategic counter-plays.
    """
    response = get_ai_response(prompt)
    if not response or 'reactions' not in response:
        response = {
            'reactions': [
                {'name': comp.get('name', 'Competitor A'), 'counter_move': 'Increase marketing spend to match your move', 'reasoning': 'Direct competitive response'}
                for comp in (competitors[:3] if competitors else [])
            ],
            'market_shift': 'Market dynamics shift as competitors respond to your move. Act strategically.'
        }
    return response


def get_counter_options(competitor_reactions):
    """Generate counter-response options to competitor moves"""
    return [
        "Accelerate your differentiation strategy",
        "Form strategic partnership to block competition",
        "Double down on customer acquisition",
        "Shift to a new market segment they can't reach",
        "Invest in technology/IP moat",
        "Focus on customer retention and loyalty"
    ]


LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    """Load leaderboard from file"""
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_leaderboard(leaderboard):
    """Save leaderboard to file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

def calculate_hack_score(metrics):
    """Calculate final hackathon score (0-100)"""
    return int((metrics.get('impact', 50) + metrics.get('finance', 50) + 
                (100 - metrics.get('risk', 50)) + metrics.get('trust', 60)) / 4)

def record_run(startup_data):
    """Record run in leaderboard and return rank"""
    score = calculate_hack_score(startup_data.get('metrics', {}))
    
    run_record = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'name': startup_data.get('name', 'Unknown'),
        'idea': startup_data.get('idea', '')[:50],  # Truncate for display
        'stage': startup_data.get('stage', 'idea'),
        'preset': startup_data.get('preset', 'general'),
        'score': score,
        'metrics': startup_data.get('metrics', {}),
        'mini_game_wins': startup_data.get('mini_game_wins', 0)
    }
    
    leaderboard = load_leaderboard()
    leaderboard.append(run_record)
    # Sort by score descending, keep top 100
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:100]
    save_leaderboard(leaderboard)
    
    # Find rank
    rank = next((i+1 for i, r in enumerate(leaderboard) if r['timestamp'] == run_record['timestamp']), 1)
    run_record['rank'] = rank
    return run_record

def generate_final_report(startup_data, decisions_history):
    """Generate comprehensive final report"""
    prompt = f"""
    Generate a comprehensive startup simulation report based on the user's journey.
    
    Startup: {startup_data.get('name')}
    Idea: {startup_data.get('idea')}
    Stage: {startup_data.get('stage')}
    Target Users: {startup_data.get('users')}
    Budget: {startup_data.get('budget')}
    
    Decision History: {json.dumps(decisions_history, indent=2)}
    
    Final Metrics:
    - Impact Score: {startup_data.get('metrics', {}).get('impact')}
    - Financial Sustainability: {startup_data.get('metrics', {}).get('finance')}
    - Risk Level: {startup_data.get('metrics', {}).get('risk')}
    - Stakeholder Trust: {startup_data.get('metrics', {}).get('trust')}
    
    Create a JSON report with:
    - summary: 2-3 sentence executive summary
    - strengths: Array of 3-4 key strengths from their decisions
    - weaknesses: Array of 3-4 key weaknesses or areas to improve
    - key_observations: Array of 2-3 important insights
    - recommendations: Array of 3-4 actionable next steps
    - execution_roadmap: Array of 5-6 specific steps with timelines (e.g., "Week 1: Validate 10 users")
    - success_probability: Percentage (0-100)
    - risk_assessment: "Low", "Medium", or "High"
    
    Return as JSON.
    """
    
    response = get_ai_response(prompt)
    return response

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_simulation():
    initial_metrics = {'impact': 50, 'finance': 50, 'risk': 50, 'trust': 60}

    session['startup_data'] = {
        'name': request.form.get('name', 'Unnamed Startup'),
        'idea': request.form.get('idea', ''),
        'stage': request.form.get('stage', 'idea'),
        'users': request.form.get('users', ''),
        'budget': request.form.get('budget', ''),
        'preset': request.form.get('preset', 'general'),
        'metrics': initial_metrics,
        'history': [],
        'decisions': [],
        'competitors': [],
        'risk_matrix': build_risk_matrix(initial_metrics),
        'kpi_projection': project_kpis(initial_metrics),
        'step': 0,
        'max_steps': 5,
        'mini_game_wins': 0,
        'mini_game_history': []
    }

    # Pre-generate all decisions + competitor view
    decisions = generate_decisions(session['startup_data'])
    session['startup_data']['decisions'] = decisions
    session['startup_data']['competitors'] = generate_competitor_analysis(session['startup_data'])

    return redirect(url_for('simulate'))

@app.route('/simulate')
def simulate():
    data = session.get('startup_data')
    if not data:
        return redirect(url_for('index'))
    
    current_step = data.get('step', 0)
    max_steps = data.get('max_steps', 5)
    
    # If all decisions are made, show results
    if current_step >= max_steps:
        return redirect(url_for('results'))
    
    # Get current decision
    decisions = data.get('decisions', [])
    if current_step < len(decisions):
        current_decision = decisions[current_step]
    else:
        return redirect(url_for('results'))
    
    return render_template('simulation.html', 
                         data=data,
                         decision=current_decision,
                         step_number=current_step + 1,
                         total_steps=max_steps)

@app.route('/process', methods=['POST'])
def process_decision():
    data = session.get('startup_data')
    if not data:
        return redirect(url_for('index'))
    
    choice = request.form.get('choice')
    mini_game_response = request.form.get('mini_game_response')
    current_step = data.get('step', 0)
    decisions = data.get('decisions', [])
    
    if current_step >= len(decisions):
        return redirect(url_for('results'))
    
    current_decision = decisions[current_step]
    
    # Get AI analysis of the decision
    outcomes = get_decision_outcomes(data, current_decision, choice)
    
    # Update metrics
    metric_changes = outcomes.get('metric_changes', {})
    data['metrics']['impact'] = max(0, min(100, data['metrics']['impact'] + metric_changes.get('impact', 0)))
    data['metrics']['finance'] = max(0, min(100, data['metrics']['finance'] + metric_changes.get('finance', 0)))
    data['metrics']['risk'] = max(0, min(100, data['metrics']['risk'] + metric_changes.get('risk', 0)))
    data['metrics']['trust'] = max(0, min(100, data['metrics']['trust'] + metric_changes.get('trust', 0)))
    
    # Generate competitor reactions (mini-game)
    competitor_reactions = generate_competitor_reactions(choice, data.get('competitors', []))
    
    # Store decision history
    decision_record = {
        'step': current_step + 1,
        'decision': current_decision.get('title'),
        'choice': choice,
        'insight': outcomes.get('insight'),
        'suggestion': outcomes.get('suggestion'),
        'stakeholder_reactions': outcomes.get('stakeholder_reactions', {}),
        'metric_changes': metric_changes,
        'competitor_reactions': competitor_reactions.get('reactions', []),
        'market_shift': competitor_reactions.get('market_shift', '')
    }
    
    # Handle mini-game counter-response if provided
    if mini_game_response:
        decision_record['mini_game_response'] = mini_game_response
        # Simple heuristic: certain counter-responses are better
        good_counters = ['Accelerate your differentiation strategy', 'Invest in technology/IP moat', 
                        'Form strategic partnership to block competition']
        if mini_game_response in good_counters:
            data['mini_game_wins'] += 1
            decision_record['mini_game_win'] = True
            data['metrics']['trust'] = min(100, data['metrics']['trust'] + 5)
        else:
            decision_record['mini_game_win'] = False
    
    data['history'].append(decision_record)
    
    # Update risk matrix and KPI projection after each decision
    data['risk_matrix'] = build_risk_matrix(data['metrics'])
    data['kpi_projection'] = project_kpis(data['metrics'])

    # Move to next step
    data['step'] = current_step + 1
    session.modified = True
    
    # Pass result to template with mini-game options
    counter_options = get_counter_options(competitor_reactions)
    
    # Pass result to template
    return render_template('simulation.html',
                         data=data,
                         processed=True,
                         result=outcomes,
                         decision_record=decision_record,
                         competitor_reactions=competitor_reactions,
                         counter_options=counter_options,
                         step_number=current_step + 1,
                         total_steps=data.get('max_steps', 5))

@app.route('/results')
def results():
    data = session.get('startup_data')
    if not data:
        return redirect(url_for('index'))
    
    # Generate final report
    report = generate_final_report(data, data.get('history', []))
    
    # Record run in leaderboard
    run_record = record_run(data)
    
    return render_template('results.html',
                         data=data,
                         report=report,
                         run_record=run_record)

@app.route('/api/metrics')
def get_metrics():
    data = session.get('startup_data')
    if not data:
        return jsonify({})
    return jsonify(data.get('metrics', {}))

@app.route('/leaderboard')
def leaderboard():
    """Display global leaderboard of top 10 runs"""
    leaderboard_data = load_leaderboard()[:10]
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/api/leaderboard')
def get_leaderboard():
    """API endpoint to get leaderboard JSON"""
    leaderboard_data = load_leaderboard()[:10]
    return jsonify(leaderboard_data)

@app.route('/export', methods=['GET'])
def export_report():
    data = session.get('startup_data')
    if not data:
        return jsonify({"error": "No simulation data available"}), 400

    report = generate_final_report(data, data.get('history', []))
    export_json = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'startup': {
            'name': data.get('name'),
            'idea': data.get('idea'),
            'stage': data.get('stage'),
            'users': data.get('users'),
            'budget': data.get('budget'),
            'preset': data.get('preset')
        },
        'metrics': data.get('metrics'),
        'history': data.get('history'),
        'final_report': report
    }
    return jsonify(export_json), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

