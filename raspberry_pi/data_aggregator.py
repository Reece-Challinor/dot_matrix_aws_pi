import datetime
from typing import Dict, List, Any

class BriefingFormatter:
    def __init__(self):
        self.box_chars = {
            'horizontal': '─',
            'vertical': '│',
            'top_left': '┌',
            'top_right': '┐',
            'bottom_left': '└',
            'bottom_right': '┘',
            'left_intersection': '├',
            'right_intersection': '┤',
            'top_intersection': '┬',
            'bottom_intersection': '┴',
            'cross': '┼'
        }

    def create_header(self, text: str, width: int = 50) -> str:
        border = "=" * width
        padding = (width - len(text)) // 2
        return f"{border}\n{' ' * padding}{text}\n{border}"

    def create_section_header(self, text: str, width: int = 50) -> str:
        stars = "*" * ((width - len(text) - 2) // 2)
        return f"{stars} {text} {stars}"

    def create_table(self, headers: List[str], data: List[List[Any]], col_widths: List[int]) -> str:
        result = []
        
        # Create top border
        top_border = self.box_chars['top_left']
        for i, width in enumerate(col_widths):
            top_border += self.box_chars['horizontal'] * width
            top_border += self.box_chars['top_right'] if i == len(col_widths)-1 else self.box_chars['top_intersection']
        result.append(top_border)
        
        # Add headers
        header_row = self.box_chars['vertical']
        for header, width in zip(headers, col_widths):
            header_row += f"{header:<{width}}"
            header_row += self.box_chars['vertical']
        result.append(header_row)
        
        # Add separator
        separator = self.box_chars['left_intersection']
        for i, width in enumerate(col_widths):
            separator += self.box_chars['horizontal'] * width
            separator += self.box_chars['right_intersection'] if i == len(col_widths)-1 else self.box_chars['cross']
        result.append(separator)
        
        # Add data rows
        for row in data:
            data_row = self.box_chars['vertical']
            for value, width in zip(row, col_widths):
                data_row += f"{str(value):<{width}}"
                data_row += self.box_chars['vertical']
            result.append(data_row)
        
        # Add bottom border
        bottom_border = self.box_chars['bottom_left']
        for i, width in enumerate(col_widths):
            bottom_border += self.box_chars['horizontal'] * width
            bottom_border += self.box_chars['bottom_right'] if i == len(col_widths)-1 else self.box_chars['bottom_intersection']
        result.append(bottom_border)
        
        return "\n".join(result)

    def create_bar_chart(self, value: float, max_value: float, width: int = 10) -> str:
        filled_blocks = int((value / max_value) * width)
        return "▇" * filled_blocks

    def format_briefing(self, data: Dict[str, Any]) -> str:
        # Initialize the briefing with the main header
        briefing = [
            self.create_header("DAILY SECURITY INTELLIGENCE BRIEFING"),
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}             Location: {data.get('location', 'N/A')}",
            f"Classification: {data.get('classification', 'CONFIDENTIAL')}",
            "=" * 50,
            ""
        ]

        # Strategic Overview
        briefing.extend([
            self.create_section_header("STRATEGIC OVERVIEW"),
            f"- Today's sentiment: {data.get('sentiment', 'N/A')}",
            f"- Weather affecting transportation: {data.get('weather_impact', 'N/A')}",
            f"- Security alerts: {data.get('security_level', 'N/A')}",
            "*" * 50,
            ""
        ])

        # Market Analysis
        if 'market_data' in data:
            briefing.extend([
                self.create_section_header("MARKET ANALYSIS"),
                "-- STOCK INDICES --"
            ])
            
            # Create market data table
            headers = ["Index", "Current", "Change"]
            market_data = [
                ["Dow Jones", data['market_data'].get('dow_value', 'N/A'), data['market_data'].get('dow_change', 'N/A')],
                ["S&P 500", data['market_data'].get('sp_value', 'N/A'), data['market_data'].get('sp_change', 'N/A')],
                ["NASDAQ", data['market_data'].get('nasdaq_value', 'N/A'), data['market_data'].get('nasdaq_change', 'N/A')]
            ]
            briefing.append(self.create_table(headers, market_data, [12, 10, 10]))
            
            # Add commodity trends
            briefing.extend([
                "-- COMMODITY TREND --",
                f"Gold: ${data['market_data'].get('gold_price', 'N/A')}/oz {self.create_bar_chart(float(data['market_data'].get('gold_trend', 0)), 100, 7)} {data['market_data'].get('gold_direction', 'N/A')}",
                f"Crude Oil: ${data['market_data'].get('oil_price', 'N/A')}/bbl {self.create_bar_chart(float(data['market_data'].get('oil_trend', 0)), 100, 5)} {data['market_data'].get('oil_direction', 'N/A')}",
                "*" * 50,
                ""
            ])

        # Add remaining sections with proper formatting
        sections = [
            ('SUPPLY CHAIN & LOGISTICS', 'supply_chain'),
            ('MILITARY DEVELOPMENTS', 'military'),
            ('GLOBAL HEADLINES', 'headlines'),
            ('ACTIONABLE RECOMMENDATIONS', 'recommendations')
        ]

        for section_title, key in sections:
            if key in data:
                briefing.extend([
                    self.create_section_header(section_title),
                    *[f"- {item}" for item in data[key]],
                    "*" * 50,
                    ""
                ])

        # Add footer
        briefing.extend([
            "=" * 50,
            "End of Briefing - Confidential Information",
            "For inquiries contact: security@yourdomain.com",
            "*" * 50
        ])

        return "\n".join(briefing)


def format_data_for_printing(data: Dict[str, Any]) -> str:
    """
    Main function to format the intelligence briefing data
    
    Args:
        data (Dict[str, Any]): Dictionary containing all the briefing data
    
    Returns:
        str: Formatted briefing ready for printing
    """
    formatter = BriefingFormatter()
    return formatter.format_briefing(data)


# Example usage
if __name__ == "__main__":
    sample_data = {
        "location": "Plano, TX",
        "classification": "CONFIDENTIAL",
        "sentiment": "CAUTIOUS, ELEVATED RISKS",
        "weather_impact": "MODERATE",
        "security_level": "ELEVATED",
        "market_data": {
            "dow_value": "28,500",
            "dow_change": "+0.5%",
            "sp_value": "3,500",
            "sp_change": "+0.3%",
            "nasdaq_value": "10,500",
            "nasdaq_change": "-0.2%",
            "gold_price": "1,800",
            "gold_trend": "70",
            "gold_direction": "Rising",
            "oil_price": "40",
            "oil_trend": "50",
            "oil_direction": "Stable"
        },
        "supply_chain": [
            "Port Congestion: LOW, container costs easing",
            "Semiconductor Shortages: PERSISTING",
            "Shipping Status: Atlantic Route: Moderate activity, clear"
        ],
        "military": [
            "Lockheed awarded $5B defense contract",
            "China increases naval production",
            "Russia/Ukraine border tension escalated"
        ],
        "headlines": [
            "Middle East: Ceasefire reached",
            "UN Climate Summit: Agreement on emission reduction"
        ],
        "recommendations": [
            "Hold energy stocks; volatility expected",
            "Avoid travel to Russia-Ukraine border region"
        ]
    }
    
    print(format_data_for_printing(sample_data))